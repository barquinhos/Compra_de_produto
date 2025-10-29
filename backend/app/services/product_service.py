from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect

from app.db_models import Category
from app import db_models
from app.models.product import ProductCreate  

def _product_has_columns(*names: str) -> bool:
    cols = set(inspect(db_models.Product).columns.keys())
    return set(names).issubset(cols)

def create_new_product(db: Session, product_data: ProductCreate) -> db_models.Product:
  
    category = db.query(Category).filter(
        Category.name == product_data.prod_category_id
    ).first()
    
    if not category:
        raise ValueError("category-not-found")

    # category = db.get(db_models.Category, product_data.prod_category_id)
    # if not category:
    #     raise ValueError("category-not-found")
  
    data = product_data.model_dump()
    
    obj = db_models.Product(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_product_item(db: Session, item_id: int) -> db_models.Product:
    item = db.get(db_models.Product, item_id)
    if not item:
        raise ValueError("product-not-found")
    return item

def list_products(
    db: Session, 
    category: Optional[int] = None,
    page: int = 1,
    size: int = 50
) -> List[db_models.Product]:
    
    q = db.query(db_models.Product)
    
    if category is not None:
        q = q.filter(db_models.Product.prod_category_id == category)
    
    if _product_has_columns("prod_name"):
        q = q.order_by(db_models.Product.prod_name)
    else:
        q = q.order_by(db_models.Product.prod_id)
    
    return q.offset((page - 1) * size).limit(size).all()

def update_product(
    db: Session, 
    product_id: int, 
    product_data: dict
) -> db_models.Product:
    product = get_product_item(db, product_id)
    
    for key, value in product_data.items():
        if hasattr(product, key) and value is not None:
            setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int) -> None:
    product = get_product_item(db, product_id)
    db.delete(product)
    db.commit()