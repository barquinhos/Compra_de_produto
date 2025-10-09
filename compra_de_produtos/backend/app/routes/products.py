from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database.session import get_db
from models.product import Product, Category
from schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductList,
    CategoryCreate, CategoryUpdate, CategoryResponse
)
from utils.dependencies import get_current_user, get_current_admin
from models.user import User

router = APIRouter()

# 📍 ROTAS PÚBLICAS (sem autenticação)
@router.get("/products/", response_model=ProductList)
async def list_products(
    skip: int = Query(0, ge=0, description="Pular registros"),
    limit: int = Query(20, ge=1, le=100, description="Limite por página"),
    category_id: Optional[int] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lista todos os produtos ativos (público)"""
    from services.product_service import ProductService
    
    return ProductService.list_products(
        db, skip, limit, category_id, featured, search
    )

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Busca um produto específico por ID (público)"""
    from services.product_service import ProductService
    
    product = ProductService.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return product

@router.get("/categories/", response_model=List[CategoryResponse])
async def list_categories(db: Session = Depends(get_db)):
    """Lista todas as categorias ativas (público)"""
    categories = db.query(Category).filter(Category.is_active == True).all()
    return categories

# 📍 ROTAS ADMIN (requer autenticação de admin)
@router.post("/products/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Cria um novo produto (apenas admin)"""
    from services.product_service import ProductService
    
    return ProductService.create_product(db, product_data)

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Atualiza um produto (apenas admin)"""
    from services.product_service import ProductService
    
    product = ProductService.update_product(db, product_id, product_data)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return product

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Desativa um produto (soft delete - apenas admin)"""
    from services.product_service import ProductService
    
    success = ProductService.delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return {"message": "Produto desativado com sucesso"}

# 📍 ROTAS CATEGORIAS (admin)
@router.post("/categories/", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Cria uma nova categoria (apenas admin)"""
    # Verificar se categoria já existe
    existing_category = db.query(Category).filter(
        Category.name == category_data.name
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria já existe"
        )
    
    db_category = Category(**category_data.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category