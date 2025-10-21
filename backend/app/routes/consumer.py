from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import List
from ..database.session import get_db
from ..models import db_models
from ..models.consumer import ConsumerCreate, ConsumerOut, ConsumerLogin, Token
from ..utils.security import get_password_hash, verify_password, create_access_token
from backend.app.services.auth_service import authenticate_consumer

router = APIRouter(prefix="/auth", tags=["Autenticação de Consumidores"])

@router.post("/register", response_model=ConsumerOut, status_code=status.HTTP_201_CREATED)
def register_customer(payload: ConsumerCreate, db: Session = Depends(get_db)):

    hashed_password = get_password_hash(payload.con_password)
    new_customer = db_models.Consumers(
        con_name=payload.con_name,
        con_email=payload.con_email.lower(),
        con_password=hashed_password
    )
    db.add(new_customer)
    try:
        db.commit()
        db.refresh(new_customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um consumidor com este e-mail já existe."
        )
    return new_customer

@router.post("/login", response_model=Token)
def login_for_consumer_access_token(payload: ConsumerLogin, db: Session = Depends(get_db)):
    
    try:
        access_token = authenticate_consumer(db, payload.con_email, payload.con_password)
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        if str(e) == "invalid-credentials":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha de consumidor incorretos",
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno no servidor")