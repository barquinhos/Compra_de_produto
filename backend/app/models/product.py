from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import Optional
import enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from backend.app.models.db_models import Category

class ProductBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    prod_name: str = Field(..., min_length=3, max_length=100, description="Nome do Produto")
    prod_description: Optional[str] = Field(None, max_length=500, description="Descrição do Produto")
    prod_price: float = Field(..., gt=0, description="Preço do Produto")
    prod_category: Category = Field(..., description="Categoria do Produto - CATEGORY_A, CATEGORY_B ou CATEGORY_C")

class ProductCreate(ProductBase):

    model_config = ConfigDict(from_attributes=True)

class ProductOut(ProductBase):

    prod_id: int
    model_config = ConfigDict(from_attributes=True)