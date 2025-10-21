from sqlalchemy.orm import Session
from backend.app.models import db_models
from backend.app.utils.security import verify_password, create_access_token

def authenticate_consumer(db: Session, email: str, password: str) -> str:

    consumer = db.query(db_models.Consumers).filter(
        db_models.Consumers.con_email == email.lower()
    ).first()

    if not consumer or not verify_password(password, consumer.con_password):
        raise ValueError("invalid-credentials")

    token_data = {"sub": str(consumer.cus_id), "scope": "customer"}
    access_token = create_access_token(subject=token_data)
    return access_token

def authenticate_seller(db: Session, email: str, password: str) -> str:

    seller_user = db.query(db_models.SellerUser).filter(
        db_models.SellerUser.sel_email == email.lower()
    ).first()

    if not seller_user or not verify_password(password, seller_user.sel_password):
        raise ValueError("invalid-credentials")

    token_data = {"sub": str(seller_user.sel_id), "scope": "seller"}
    access_token = create_access_token(subject=token_data)
    return access_token