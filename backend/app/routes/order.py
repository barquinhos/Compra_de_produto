from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database.session import get_db
from models import db_models
from models.order import OrderCreate, OrderOut
from utils.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Pedidos"])

@router.post("/checkout", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def checkout(
    checkout_data: OrderCreate,
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db)
):    
    cart = db.query(db_models.Cart).filter(db_models.Cart.con_id == current_user.con_id).first()
    
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Carrinho vazio"
        )
    
    total_amount = 0.0
    
    for cart_item in cart.items:
        product = cart_item.product
        
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para {product.prod_name}"
            )
        
        product.stock -= cart_item.quantity
        subtotal = float(product.prod_price) * cart_item.quantity
        total_amount += subtotal

    order = db_models.Order(
        con_id=current_user.con_id,
        ord_total_amount=total_amount,
        ord_status=db_models.OrderStatus.PENDING
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for cart_item in cart.items:
        product = cart_item.product
        subtotal = float(product.prod_price) * cart_item.quantity
        
        order_item = db_models.OrderItem(
            ord_id=order.ord_id,
            prod_id=product.prod_id,
            prod_name=product.prod_name,
            unit_price=float(product.prod_price),
            quantity=cart_item.quantity,
            orit_subtotal=subtotal
        )
        db.add(order_item)
    
    db.query(db_models.CartItem).filter(db_models.CartItem.cart_id == cart.car_id).delete()
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/", response_model=List[OrderOut])
def get_user_orders(
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    orders = db.query(db_models.Order).filter(
        db_models.Order.con_id == current_user.con_id
    ).order_by(db_models.Order.ord_id.desc()).offset(skip).limit(limit).all()
    
    return orders

@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(db_models.Order).filter(
        db_models.Order.ord_id == order_id,
        db_models.Order.con_id == current_user.con_id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    
    return order