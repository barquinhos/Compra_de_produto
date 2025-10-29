from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.session import Base, engine
from app.routes import auth, cart, consumer, order, products

Base.metadata.create_all(bind=engine)

app = FastAPI() 

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

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(order.router)
app.include_router(consumer.router)

