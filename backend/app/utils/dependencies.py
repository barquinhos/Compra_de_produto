from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from ..database.session import get_db
from ..models import db_models
from ..utils.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> db_models.Consumers | db_models.SellerUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        scope: str = payload.get("scope")
        if user_id is None or scope is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = None
    if scope == "customer":
        user = db.get(db_models.Consumers, int(user_id))
    elif scope == "seller":
        user = db.get(db_models.SellerUser, int(user_id))

    if user is None:
        raise credentials_exception
        
    return user

def get_current_consumer(
    current_user: db_models.Consumers = Depends(get_current_user)
) -> db_models.Consumers:
    if not isinstance(current_user, db_models.Consumers):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Operation not permitted for this user type"
        )
    return current_user

def get_current_seller_user(
    current_user: db_models.SellerUser = Depends(get_current_user)
) -> db_models.SellerUser:
    if not isinstance(current_user, db_models.SellerUser):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Operation not permitted for this user type"
        )
    return current_user