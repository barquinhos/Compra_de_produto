from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.database import engine, Base
from routes import auth, cart, consumer, order, products


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API do Sistema de Compras de Produtos",
    description="API para gerenciar compras, consumidores e produtos.",
    version="0.1.0"
)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
        from routes import auth, cart, consumer, order, products
except ImportError as e:
        print(f"Error importing routes: {e}")
        raise

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(consumer.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API de Compras de Produtos!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API está funcionando"}