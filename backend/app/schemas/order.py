from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "aguardando_pagamento"
    PAID = "pago"
    SHIPPED = "enviado"
    DELIVERED = "entregue"
    CANCELLED = "cancelado"

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('A quantidade deve ser maior que zero')
        return v

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    subtotal: float
    product_name: str
    product_price: float
    product_image: Optional[str] = None

    class Config:
        orm_mode = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    items: List[CartItemResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    subtotal: float

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    shipping_address: str

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    order_number: str
    total_amount: float
    status: OrderStatus
    shipping_address: str
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int
    skip: int
    limit: int

class CheckoutRequest(BaseModel):
    shipping_address: str

class CheckoutResponse(BaseModel):
    order: OrderResponse
    message: str