from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# SCHEMAS BASE
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock: int = 0
    sku: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: bool = False

# SCHEMAS DE CRIAÇÃO
class CategoryCreate(CategoryBase):
    pass

class ProductCreate(ProductBase):
    pass

# SCHEMAS DE ATUALIZAÇÃO
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    sku: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None

# SCHEMAS DE RESPOSTA
class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    model_config = ConfigDict(from_attributes=True)

# SCHEMAS PARA LISTAGEM
class ProductList(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    pages: int