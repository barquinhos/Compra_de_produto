from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database.session import get_db
from ..models.user import User
from ..schemas.user import UserResponse
from ..schemas.order import OrderResponse
from ..utils.dependencies import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém o perfil do usuário logado"""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_data = user_data.dict(exclude_unset=True)
    if 'email' in update_data and update_data['email'] != current_user.email:
        existing_user = db.query(User).filter(
            User.email == update_data['email'],
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/orders", response_model=List[OrderResponse])
async def get_user_orders(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista os pedidos do usuário logado"""
    from ..models.order import Order
    
    orders = db.query(Order).filter(
        Order.user_id == current_user.id,
        Order.is_active == True
    ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    return orders