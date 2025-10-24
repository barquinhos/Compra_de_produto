from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.app.session import get_db
from backend.app import db_models
from models.seller import SellerCreate, SellerOut, SellerLogin
from models.consumer import Token
from utils.security import get_password_hash, verify_password, create_access_token
from services.auth_service import authenticate_seller

router = APIRouter(prefix="/seller/auth", tags=["Autenticação de Vendedores"])

@router.post("/register", response_model=SellerOut, status_code=status.HTTP_201_CREATED)
def register_seller_user(payload: SellerCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(payload.sel_password)
    new_seller_user = db_models.SellerUser(
        sel_email=payload.sel_email,
        sel_password=hashed_password,
        sel_name=payload.sel_name,
    )
    
    db.add(new_seller_user)
    try:
        db.commit()
        db.refresh(new_seller_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email já está em uso"
        )
    return new_seller_user

@router.post("/login", response_model=Token)
def login_for_seller_access_token(payload: SellerLogin, db: Session = Depends(get_db)):
    try:
        access_token = authenticate_seller(db, payload.sel_email, payload.sel_password)

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError as e:
        if str(e) == "invalid-credentials":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha de vendedor incorretos",
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")