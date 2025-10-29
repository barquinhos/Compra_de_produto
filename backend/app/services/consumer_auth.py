from sqlalchemy.orm import Session
from sqlalchemy import func
from app import db_models
from app.utils.security import verify_password, create_access_token

# def authenticate_consumer(db: Session, email: str, password: str) -> 

#     consumer = db.query(db_models.Consumers).filter(
#         db_models.Consumers.con_email == email.lower()
#     ).first()

#     if not consumer or not verify_password(password, consumer.con_password):
#         raise ValueError("invalid-credentials")

#     token_data = {"sub": str(consumer.con_id), "scope": "consumer"}
#     access_token = create_access_token(subject=token_data)
#     return access_token

def authenticate_consumer(db: Session, email: str, password: str) -> tuple[db_models.Consumers, str]:
    consumer = db.query(db_models.Consumers).filter(
        func.lower(db_models.Consumers.con_email) == email.lower()
    ).first()

    if not consumer or not verify_password(password, consumer.con_password):
        raise ValueError("invalid-credentials")

    token_data = {
        "sub": str(consumer.con_id), 
        "scope": "consumer",
        "email": consumer.con_email,
        "name": consumer.con_name  
    }
    access_token = create_access_token(subject=token_data)
    
    return consumer, access_token