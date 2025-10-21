import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(__file__))

# Caminho absoluto para o banco
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

print(f"📁 Criando banco em: {DATABASE_URL}")

# Cria engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Cria SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define os modelos manualmente
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Enum, Numeric
import enum

class OrderStatus(enum.Enum):
    PENDING = "aguardando_pagamento"
    PAID = "pago"
    SHIPPED = "enviado"
    DELIVERED = "entregue"
    CANCELLED = "cancelado"

class Consumers(Base):
    __tablename__ = "consumers"
    con_id = Column(Integer, primary_key=True, index=True)
    con_name = Column(String(100), nullable=False)
    con_email = Column(String(255), nullable=False, unique=True, index=True)
    con_password = Column(String(255), nullable=False)

class SellerUser(Base):
    __tablename__ = "seller_users"
    sel_id = Column(Integer, primary_key=True, index=True)
    sel_name = Column(String(100), nullable=False)
    sel_email = Column(String(255), nullable=False, unique=True, index=True)
    sel_password = Column(String(255), nullable=False)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

class Product(Base):
    __tablename__ = "products"
    prod_id = Column(Integer, primary_key=True, index=True)
    prod_name = Column(String(200), nullable=False)
    description = Column(Text)
    prod_price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    prod_category_id = Column(Integer, ForeignKey("categories.id"))

class Cart(Base):
    __tablename__ = "carts"
    car_id = Column(Integer, primary_key=True, index=True)
    con_id = Column(Integer, ForeignKey("consumers.con_id"), unique=True, nullable=False)

class CartItem(Base):
    __tablename__ = "cart_items"
    carit_id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("carts.car_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.prod_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

class Order(Base):
    __tablename__ = "orders"
    ord_id = Column(Integer, primary_key=True, index=True)
    con_id = Column(Integer, ForeignKey("consumers.con_id"), nullable=False)
    car_id = Column(Integer, ForeignKey("carts.car_id"), nullable=False)
    ord_total_amount = Column(Numeric(10, 2), nullable=False)
    ord_status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    shipping_address = Column(Text, nullable=False)

class OrderItem(Base):
    __tablename__ = "order_items"
    orit_id = Column(Integer, primary_key=True, index=True)
    ord_id = Column(Integer, ForeignKey("orders.ord_id"), nullable=False)
    prod_id = Column(Integer, ForeignKey("products.prod_id"), nullable=False)
    prod_name = Column(String(200), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    orit_subtotal = Column(Numeric(10, 2), nullable=False)

# Criação das tabelas (opcional - pode ser feito separadamente)
def create_tables():
    print("🔄 Criando banco de dados e tabelas...")
    try:
        # Cria todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("✅ BANCO DE DADOS CRIADO COM SUCESSO!")
        print("📊 TABELAS CRIADAS:")
        for table_name in Base.metadata.tables.keys():
            print(f"   ✅ {table_name}")

        # Verifica se o arquivo foi criado
        if os.path.exists(os.path.join(BASE_DIR, 'app.db')):
            print(f"📁 Arquivo do banco criado: app.db")
            print(f"📏 Tamanho: {os.path.getsize(os.path.join(BASE_DIR, 'app.db'))} bytes")
        else:
            print("❌ Arquivo do banco não foi criado")

    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

# Executa a criação das tabelas apenas se o script for executado diretamente
if __name__ == "__main__":
    create_tables()