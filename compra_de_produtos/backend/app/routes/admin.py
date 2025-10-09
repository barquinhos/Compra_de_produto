from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.user import User
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate
from utils.dependencies import get_current_admin  

router = APIRouter()

@router.post("/products/")
async def admin_create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_admin),  
    db: Session = Depends(get_db)
):
    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/dashboard")
async def admin_dashboard(
    current_user: User = Depends(get_current_admin),  
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    total_products = db.query(Product).filter(Product.is_active == True).count()
    
    return {
        "total_users": total_users,
        "total_products": total_products,
        "admin_email": current_user.email
    }