from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from app.session import get_db
from app.models.product import ProductCreate, ProductOut
from app.db_models import Category
from app.services.product_service import create_new_product, list_products
from app.services import product_service

router = APIRouter()

@router.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        return product_service.create_new_product(db, product)
    except ValueError as e:
        if str(e) == "category-not-found":
            raise HTTPException(status_code=404, detail="Category not found")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return product_service.get_product_item(db, product_id)
    except ValueError as e:
        if str(e) == "product-not-found":
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products/")
def list_products(
    category: Optional[int] = None,
    page: int = 1,
    size: int = 50,
    db: Session = Depends(get_db)
):
    return product_service.list_products(db, category, page, size)

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product_service.delete_product(db, product_id)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        if str(e) == "product-not-found":
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(status_code=400, detail=str(e))