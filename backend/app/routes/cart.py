from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.session import get_db
from app import db_models
from app.models.cart import CartItemCreate, CartItemUpdate, CartOut
from app.utils.dependencies import get_current_user
from app.services.cart_service import cart_service

router = APIRouter(prefix="/cart", tags=["Carrinho"])

@router.get("/", response_model=CartOut)
def get_cart(
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.get_or_create_cart(db, current_user.con_id)

@router.post("/items", response_model=CartOut)
def add_to_cart(
    item_data: CartItemCreate,
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.add_item_to_cart(db, current_user.con_id, item_data)

@router.put("/items/{item_id}", response_model=CartOut)
def update_cart_item(
    item_id: int,
    item_data: CartItemUpdate,
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.update_cart_item(db, current_user.con_id, item_id, item_data)

@router.delete("/items/{item_id}", response_model=CartOut)
def remove_from_cart(
    item_id: int,
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.remove_item_from_cart(db, current_user.con_id, item_id)

@router.delete("/")
def clear_cart(
    current_user: db_models.Consumers = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return cart_service.clear_cart(db, current_user.con_id)