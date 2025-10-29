from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Boolean, 
    Float, 
    ForeignKey, 
    Numeric, 
    UniqueConstraint,
    Enum,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.session import Base
import enum

class Consumers(Base):

    __tablename__ = "consumers"
    __table_args__ = (UniqueConstraint("con_email", name="uq_consumers_email"),)

    con_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    con_name: Mapped[str] = mapped_column(String(100), nullable=False)
    con_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    con_password: Mapped[str] = mapped_column(String(255), nullable=False)

    orders: Mapped[list["Order"]] = relationship(back_populates="consumer")
    carts: Mapped[list["Cart"]] = relationship(back_populates="consumer")

class SellerUser(Base):
    
    __tablename__ = "seller_users"
    __table_args__ = (UniqueConstraint("sel_email", name="uq_seller_users_email"),)

    sel_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sel_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sel_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    sel_password: Mapped[str] = mapped_column(String(255), nullable=False)

class Product(Base):
    __tablename__ = "products"
    
    prod_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prod_name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    prod_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  
    stock: Mapped[int] = mapped_column(Integer, default=0)
    prod_category_id: Mapped[str] = mapped_column(String(50), ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship(back_populates="products")
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")

class Category(Base):  
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

class OrderStatus(enum.Enum):
    PENDING = "aguardando_pagamento"
    PAID = "pago"
    SHIPPED = "enviado"
    DELIVERED = "entregue"
    CANCELLED = "cancelado"

class Cart(Base):
    __tablename__ = "carts"
    __table_args__ = (UniqueConstraint("con_id", name="uq_carts_consumer_id"),)


    car_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    con_id: Mapped[int] = mapped_column(ForeignKey("consumers.con_id"), unique=True, nullable=False)

    consumer: Mapped["Consumers"] = relationship(back_populates="carts")
    items: Mapped[list["CartItem"]] = relationship(back_populates="cart")
    orders: Mapped[list["Order"]] = relationship(back_populates="cart")

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items)

class CartItem(Base):
    __tablename__ = "cart_items"

    carit_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("carts.car_id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.prod_id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    cart: Mapped["Cart"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="cart_items",lazy="joined")

    @property
    def subtotal(self):
        return self.product.prod_price * self.quantity

class Order(Base):

    __tablename__ = "orders"
    
    ord_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    con_id: Mapped[int] = mapped_column(ForeignKey("consumers.con_id"), nullable=False)
    car_id: Mapped[int] = mapped_column(ForeignKey("carts.car_id"), nullable=False)
    ord_total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    ord_status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    shipping_address: Mapped[str] = mapped_column(Text, nullable=False)

    consumer: Mapped["Consumers"] = relationship(back_populates="orders")
    cart: Mapped["Cart"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    orit_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ord_id: Mapped[int] = mapped_column(ForeignKey("orders.ord_id"), nullable=False)
    prod_id: Mapped[int] = mapped_column(ForeignKey("products.prod_id"), nullable=False)
    prod_name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2),nullable=False)  
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    orit_subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items",lazy="joined")