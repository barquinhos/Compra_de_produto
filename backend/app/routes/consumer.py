from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import List
from app.session import get_db
from app import db_models
from app.models.consumer import ConsumerCreate, ConsumerOut, ConsumerLogin, Token
from app.utils.security import get_password_hash, verify_password, create_access_token
from app.services.consumer_auth import authenticate_consumer

router = APIRouter(prefix="/auth", tags=["Autenticação de Consumidores"])

@router.post("/register", response_model=ConsumerOut, status_code=status.HTTP_201_CREATED)
def register_consumer(payload: ConsumerCreate, db: Session = Depends(get_db)):
  
    name_norm = payload.con_name.strip()
    email_norm = payload.con_email.lower().strip()

    
    exists = db.query(db_models.Consumers).filter(
        func.lower(db_models.Consumers.con_email) == email_norm
    ).first()

    if exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um consumidor com este e-mail já existe."
        )
    
    new_consumer = db_models.Consumers(
        con_name=name_norm,
        con_email=email_norm,
        con_password=get_password_hash(payload.con_password)
    )
    
    db.add(new_consumer)
    db.commit()
    db.refresh(new_consumer)
    return new_consumer

@router.post("/login", response_model=dict)
def login_for_consumer_access_token(payload: ConsumerLogin, db: Session = Depends(get_db)):
    try:
        
        consumer, access_token = authenticate_consumer(db, payload.con_email, payload.con_password)
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "consumer": ConsumerOut.from_orm(consumer)  
        }

    except ValueError as e:
        if str(e) == "invalid-credentials":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha de consumidor incorretos",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno no servidor"
        )