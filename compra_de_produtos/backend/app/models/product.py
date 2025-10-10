from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.session import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relação com produtos
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)  # 10 dígitos, 2 decimais
    stock = Column(Integer, default=0)
    sku = Column(String(100), unique=True)  # Código único do produto
    image_url = Column(String(500))  # URL da imagem
    
    # Chave estrangeira para categoria
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Status do produto
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relações
    category = relationship("Category", back_populates="products")
    
    def soft_delete(self):
        """Marca o produto como inativo (soft delete)"""
        self.is_active = False
        self.updated_at = datetime.utcnow()