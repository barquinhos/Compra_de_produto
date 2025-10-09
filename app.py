from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Finalmente funcionando! 🎉"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/auth/register")
async def register_user(username: str, email: str, password: str):
    return {
        "message": "Usuário registrado com sucesso",
        "user": {"username": username, "email": email}
    }

@app.post("/auth/login")
async def login_user(email: str, password: str):
    return {
        "message": "Login realizado com sucesso",
        "user": {"email": email},
        "token": "jwt_token_exemplo"
    }

# Rotas de produtos
@app.get("/products/")
async def list_products():
    return {
        "products": [
            {"id": 1, "name": "Produto A", "price": 29.99},
            {"id": 2, "name": "Produto B", "price": 49.99}
        ]
    }

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    return {
        "id": product_id,
        "name": f"Produto {product_id}",
        "price": 99.99,
        "description": "Descrição do produto"
    }

@app.post("/products/")
async def create_product(name: str, price: float):
    return {
        "message": "Produto criado com sucesso",
        "product": {"name": name, "price": price}
    }