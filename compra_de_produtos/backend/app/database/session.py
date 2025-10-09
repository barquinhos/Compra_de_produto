from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, 
    pool_size=10,           # Número máximo de conexões no pool
    max_overflow=20,        # Conexões extras temporárias
    pool_pre_ping=True,     # Verifica se conexão está ativa
    echo=True              # Mostra SQL no console (remova em produção)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()