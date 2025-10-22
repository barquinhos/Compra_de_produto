from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from models import db_models
from models.product import Category

def create_new_product(db: Session, product_data: dict) -> db_models.Product:
    new_product = db_models.Product(**product_data)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def get_product_item(db: Session, item_id: int) -> db_models.Product:
    item = db.get(db_models.Product, item_id)
    if not item:
        raise ValueError("item-not-found")
    return item

def list_products(db: Session, category: Optional[Category] = None):
    query = db.query(db_models.Product)
    if category:
        query = query.filter(db_models.Product.prod_category_id == category)
    return query.all()

def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(db_models.Product).filter(db_models.Product.id == product_id).first()
    if not product:
        return False
    
    product.soft_delete()
    db.commit()
    return True