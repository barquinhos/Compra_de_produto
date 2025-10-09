from fastapi import FastAPI
from database.session import engine, Base
from routes import auth, products

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Compra de Produtos",
    description="API para gerenciamento de e-commerce",
    version="1.0.0"
)

# Incluir rotas
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(products.router, prefix="/products", tags=["Produtos"])

@app.get("/")
async def root():
    return {"message": "Sistema de Compra de Produtos API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}