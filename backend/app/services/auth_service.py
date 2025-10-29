from sqlalchemy.orm import Session
from sqlalchemy import func
from app import db_models
from app.utils.security import verify_password, create_access_token

# def authenticate_seller(db: Session, email: str, password: str) -> str:

#     seller_user = db.query(db_models.SellerUser).filter(
#         db_models.SellerUser.sel_email == email.lower()
#     ).first()

#     if not seller_user or not verify_password(password, seller_user.sel_password):
#         raise ValueError("invalid-credentials")

#     token_data = {"sub": str(seller_user.sel_id), "scope": "seller"}
#     access_token = create_access_token(subject=token_data)
#     return access_token

def authenticate_seller(db: Session, email: str, password: str) -> tuple[db_models.SellerUser, str]:
    seller_user = db.query(db_models.SellerUser).filter(
        func.lower(db_models.SellerUser.sel_email) == email.lower()
    ).first()

    if not seller_user:
        raise ValueError("invalid-credentials")

    if not verify_password(password, seller_user.sel_password):
        raise ValueError("invalid-credentials")

    token_data = {
        "sub": str(seller_user.sel_id), 
        "scope": "seller",
        "email": seller_user.sel_email,
        "name": seller_user.sel_name  
    }
    access_token = create_access_token(subject=token_data)
    
    return seller_user, access_token