from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..models.user import User
from ..models.order import Order, OrderItem, OrderStatus, Cart, CartItem
from ..models.product import Product
from ..schemas.order import (
    OrderResponse, OrderListResponse, CheckoutRequest, CheckoutResponse
)
from ..utils.dependencies import get_current_user, get_current_admin
from typing import Optional
from ..schemas.order import OrderUpdate

router = APIRouter()

@router.post("/orders/checkout", response_model=CheckoutResponse)
async def checkout(
    checkout_data: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Processa checkout e cria pedido"""
    # Obtém carrinho do usuário
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Carrinho vazio"
        )
    
    # Verifica estoque e calcula total
    total_amount = 0
    order_items_data = []
    
    for cart_item in cart.items:
        product = cart_item.product
        
        # Verifica estoque
        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para {product.name}"
            )
        
        # Atualiza estoque
        product.stock -= cart_item.quantity
        
        # Calcula subtotal
        subtotal = float(product.price) * cart_item.quantity
        total_amount += subtotal
        
        # Prepara dados do item do pedido
        order_items_data.append({
            'product_id': product.id,
            'product_name': product.name,
            'product_price': float(product.price),
            'quantity': cart_item.quantity,
            'subtotal': subtotal
        })
    
    # Gera número do pedido
    from datetime import datetime
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{current_user.id:06d}"
    
    # Cria pedido
    order = Order(
        user_id=current_user.id,
        order_number=order_number,
        total_amount=total_amount,
        shipping_address=checkout_data.shipping_address,
        status=OrderStatus.PENDING
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Cria itens do pedido
    for item_data in order_items_data:
        order_item = OrderItem(order_id=order.id, **item_data)
        db.add(order_item)
    
    # Limpa carrinho
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(order)
    
    return CheckoutResponse(
        order=order,
        message="Pedido criado com sucesso. Aguardando pagamento."
    )

@router.get("/orders", response_model=List[OrderResponse])
async def get_user_orders(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista pedidos do usuário logado"""
    orders = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.is_active == True
    ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return orders

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém detalhes de um pedido específico"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id,
        Order.is_active == True
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    
    return order

# ROTAS ADMIN PARA PEDIDOS
@router.get("/admin/orders", response_model=List[OrderResponse])
async def list_all_orders(
    skip: int = 0,
    limit: int = 50,
    status: Optional[OrderStatus] = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Lista todos os pedidos (apenas admin)"""
    query = db.query(Order).filter(Order.is_active == True)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@router.put("/admin/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_update: OrderUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Atualiza status do pedido (apenas admin)"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.is_active == True
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )
    
    if status_update.status:
        order.status = status_update.status
    
    db.commit()
    db.refresh(order)
    return order