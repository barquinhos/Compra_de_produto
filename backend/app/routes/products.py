from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.app.session import get_db
from models.product import ProductCreate, ProductOut
from backend.app.db_models import Category
from services.product_service import create_new_product, list_products

router = APIRouter()

@router.post("/products/", response_model=ProductOut)
def create_new_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_new_product(db, product_data)

@router.get("/products/", response_model=List[ProductOut])
def list_products(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    return list_products(db, category_id)
