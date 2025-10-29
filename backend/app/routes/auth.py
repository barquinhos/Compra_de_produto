from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from app.session import get_db
from app import db_models
from app.models.seller import SellerCreate, SellerOut, SellerLogin
from app.models.consumer import Token
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.services.auth_service import authenticate_seller

router = APIRouter(prefix="/seller/auth", tags=["Autenticação de Vendedores"])

@router.post("/register", response_model=SellerOut, status_code=status.HTTP_201_CREATED)
def register_seller_user(payload: SellerCreate, db: Session = Depends(get_db)):
   
    email_norm = payload.sel_email.lower().strip()
    name_norm = payload.sel_name.strip()
    
    exists = db.query(db_models.SellerUser).filter(
        func.lower(db_models.SellerUser.sel_email) == email_norm
    ).first()
    
    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já está em uso"
        )
    
    new_seller_user = db_models.SellerUser(
        sel_email=email_norm,
        sel_password=get_password_hash(payload.sel_password),
        sel_name=name_norm,
    )
    
    db.add(new_seller_user)
    db.commit()
    db.refresh(new_seller_user)
    return new_seller_user

@router.post("/login", response_model=dict)
def login_for_seller_access_token(payload: SellerLogin, db: Session = Depends(get_db)):
    try:
        seller_user, access_token = authenticate_seller(db, payload.sel_email, payload.sel_password)
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "seller": SellerOut.from_orm(seller_user) 
        }

    except ValueError as e:
        if str(e) == "invalid-credentials":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha de vendedor incorretos",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno no servidor"
        )