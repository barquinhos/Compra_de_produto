from sqlalchemy.orm import Session
from typing import Optional, List
from models.product import Product, Category
from schemas.product import ProductCreate, ProductUpdate, ProductList
from fastapi import HTTPException

class ProductService:
    
    @staticmethod
    def list_products(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        category_id: Optional[int] = None,
        featured: Optional[bool] = None,
        search: Optional[str] = None
    ) -> ProductList:
        """Lista produtos com filtros e paginação"""
        query = db.query(Product).filter(Product.is_active == True)
        
        # Aplicar filtros
        if category_id:
            query = query.filter(Product.category_id == category_id)
        
        if featured is not None:
            query = query.filter(Product.is_featured == featured)
        
        if search:
            query = query.filter(
                Product.name.ilike(f"%{search}%") |
                Product.description.ilike(f"%{search}%")
            )
        
        # Contar total antes da paginação
        total = query.count()
        
        # Aplicar paginação
        products = query.offset(skip).limit(limit).all()
        
        # Calcular páginas
        pages = (total + limit - 1) // limit  # Arredondamento para cima
        
        return ProductList(
            products=products,
            total=total,
            page=(skip // limit) + 1,
            pages=pages
        )
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        """Busca um produto por ID (apenas ativos)"""
        return db.query(Product).filter(
            Product.id == product_id,
            Product.is_active == True
        ).first()
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        """Cria um novo produto"""
        # Verificar se SKU já existe
        if product_data.sku:
            existing_product = db.query(Product).filter(
                Product.sku == product_data.sku
            ).first()
            if existing_product:
                raise HTTPException(
                    status_code=400,
                    detail="SKU já existe"
                )
        
        db_product = Product(**product_data.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def update_product(
        db: Session, 
        product_id: int, 
        product_data: ProductUpdate
    ) -> Optional[Product]:
        """Atualiza um produto existente"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        
        # Atualizar apenas campos fornecidos
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Desativa um produto (soft delete)"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        
        product.soft_delete()
        db.commit()
        return True