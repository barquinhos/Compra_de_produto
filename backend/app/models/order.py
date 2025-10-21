from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing import List
from datetime import datetime

from .product import ProductOut
from .db_models import OrderStatus

class OrderItemBase(BaseModel):

    prod_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade do item")

class OrderCreate(BaseModel):

    items: List[OrderItemBase] = Field(..., min_length=1, description="Lista de itens do pedido")

class OrderItemOut(BaseModel):

    orit_id: int
    orit_quantity: int
    orit_unit_price: float
    product: ProductOut
    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):

    ord_id: int
    con_id: int
    car_id: int
    ord_status: OrderStatus
    ord_total_value: float
    items: List[OrderItemOut] = []
    model_config = ConfigDict(from_attributes=True)