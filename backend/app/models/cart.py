from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import List, Optional

class CartItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade do produto")

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description="Nova quantidade do produto")

class CartItemOut(BaseModel):
    carit_id: int = Field(..., description="ID do item no carrinho")
    product_id: int = Field(..., description="ID do produto")
    quantity: int = Field(..., description="Quantidade")
    product_name: str = Field(..., description="Nome do produto")
    unit_price: float = Field(..., description="Preço unitário")
    subtotal: float = Field(..., description="Subtotal do item")
    
    model_config = ConfigDict(from_attributes=True)

class CartBase(BaseModel):
    car_number: int = Field(..., gt=0, description="Número do carrinho")

class CartCreate(CartBase):
    pass

class CartOut(CartBase):
    car_id: int = Field(..., description="ID do carrinho")
    con_id: int = Field(..., description="ID do consumidor")
    items: List[CartItemOut] = Field(default_factory=list, description="Itens do carrinho")
    total_amount: float = Field(0.0, description="Valor total do carrinho")
    
    model_config = ConfigDict(from_attributes=True)