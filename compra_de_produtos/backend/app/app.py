from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os

load_dotenv()

from .database.session import engine, Base
from .routes import auth, products
from .routes.auth import router as auth_router
from .routes.products import router as products_router
from .routes.admin import router as admin_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Sistema de Compras", version="3.0")

app.include_router(admin_router)
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(products.router, prefix="/products", tags=["Produtos"])

def get_html_template() -> str:
    """Retorna o template HTML da página inicial"""
    
    endpoints_info = [
        {"method": "GET", "path": "/products/", "description": "Listar produtos"},
        {"method": "GET", "path": "/products/{id}", "description": "Obter produto específico"},
        {"method": "POST", "path": "/products/", "description": "Criar novo produto"},
        {"method": "POST", "path": "/auth/register", "description": "Registrar usuário"},
        {"method": "POST", "path": "/auth/login", "description": "Login de usuário"}
        # {"method": "POST", "path": "/admin/products/", "description": "Criar produto (Admin)"},
        # {"method": "GET", "path": "/admin/dashboard", "description": "Dashboard administrativo"}
    ]
    
    modules_info = [
        {
            "icon": "📦",
            "title": "Módulo de Produtos",
            "features": ["CRUD completo de produtos", "Filtros e busca", "Gestão de categorias", "Controle de estoque"]
        },
        {
            "icon": "👥", 
            "title": "Sistema de Usuários",
            "features": ["Registro e autenticação", "Perfis de usuário cliente e usuário administrador"]
        },
        {
            "icon": "🛒",
            "title": "Processo de Vendas", 
            "features": ["Cesta de compras", "Sistema de pedidos", "Status de entrega"]
        }
    ]
    
    stats_info = [
        {"number": "8", "label": "Endpoints", "suffix": ""},
        {"number": "3", "label": "Módulos", "suffix": ""},
        {"number": "100", "label": "Funcional", "suffix": "%"}
    ]
    
    # Gerar HTML dinamicamente
    endpoints_html = "".join(
        f'''
        <div class="endpoint-item">
            <span class="method {endpoint['method'].lower()}">{endpoint['method']}</span>
            <strong>{endpoint['path']}</strong>
            <div class="endpoint-description">{endpoint['description']}</div>
        </div>
        ''' for endpoint in endpoints_info
    )
    
    modules_html = "".join(
        f'''
        <div class="card">
            <h3>{module['icon']} {module['title']}</h3>
            <ul>
                {''.join(f'<li>{feature}</li>' for feature in module['features'])}
            </ul>
        </div>
        ''' for module in modules_info
    )
    
    stats_html = "".join(
        f'''
        <div class="stat-item">
            <span class="stat-number" data-target="{stat['number']}" data-suffix="{stat['suffix']}">0{stat['suffix']}</span>
            <span class="stat-label">{stat['label']}</span>
        </div>
        ''' for stat in stats_info
    )
    
    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="API completa para gerenciamento de loja virtual">
        <meta name="keywords" content="ecommerce, API, FastAPI, sistema de vendas">
        <title>🛒 Sistema de Compras - API v3.0</title>
        
        <!-- Open Graph -->
        <meta property="og:title" content="Sistema de Compras">
        <meta property="og:description" content="API completa para gerenciamento de loja virtual">
        <meta property="og:type" content="website">
        
        <style>
            :root {{
                --primary-color: #3498db;
                --secondary-color: #2c3e50;
                --success-color: #27ae60;
                --warning-color: #f39c12;
                --danger-color: #e74c3c;
                --text-color: #333;
                --light-bg: #f8f9fa;
                --border-radius: 10px;
                --box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                --transition: all 0.3s ease;
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
                color: var(--text-color);
                line-height: 1.6;
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: var(--border-radius);
                box-shadow: var(--box-shadow);
                overflow: hidden;
                animation: fadeIn 0.8s ease-out;
            }}
            
            .header {{
                background: linear-gradient(135deg, #2e3715, #3d4c1e);
                color: white;
                padding: 40px 30px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" opacity="0.05"><circle cx="50" cy="50" r="2" fill="white"/></svg>');
            }}
            
            .header h1 {{
                font-size: clamp(2rem, 4vw, 2.5rem);
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 15px;
                position: relative;
            }}
            
            .header p {{
                font-size: clamp(1rem, 2vw, 1.2rem);
                opacity: 0.9;
                margin-bottom: 20px;
                position: relative;
            }}
            
            .badge {{
                background: var(--danger-color);
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
                display: inline-block;
                margin-bottom: 10px;
                position: relative;
                font-weight: 600;
            }}
            
            .content {{
                padding: 40px 30px;
            }}
            
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
            }}
            
            .card {{
                background: var(--light-bg);
                border-radius: var(--border-radius);
                padding: 25px;
                border-left: 4px solid var(--primary-color);
                transition: var(--transition);
                height: 100%;
                display: flex;
                flex-direction: column;
            }}
            
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}
            
            .card h3 {{
                color: var(--secondary-color);
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 1.3rem;
            }}
            
            .card ul {{
                list-style: none;
                flex-grow: 1;
            }}
            
            .card li {{
                padding: 8px 0;
                border-bottom: 1px solid #eee;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .card li:before {{
                content: "✅";
                font-size: 0.9rem;
                flex-shrink: 0;
            }}
            
            .endpoints {{
                background: linear-gradient(135deg, #2e3715, #3d4c1e);
                color: white;
                padding: 30px;
                border-radius: var(--border-radius);
                margin-bottom: 30px;
            }}
            
            .endpoints h3 {{
                text-align: center;
                margin-bottom: 25px;
                color: #ecf0f1;
                font-size: 1.5rem;
            }}
            
            .endpoint-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
            }}
            
            .endpoint-item {{
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 8px;
                border-left: 3px solid var(--primary-color);
                transition: var(--transition);
            }}
            
            .endpoint-item:hover {{
                background: rgba(255,255,255,0.15);
                transform: translateX(5px);
            }}
            
            .method {{
                display: inline-block;
                padding: 3px 10px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 0.8rem;
                margin-right: 10px;
                font-family: 'Courier New', monospace;
            }}
            
            .get {{ background: var(--success-color); color: white; }}
            .post {{ background: var(--primary-color); color: white; }}
            .put {{ background: var(--warning-color); color: white; }}
            .delete {{ background: var(--danger-color); color: white; }}
            .patch {{ background: #9b59b6; color: white; }}
            
            .endpoint-description {{
                font-size: 0.9rem;
                margin-top: 5px;
                opacity: 0.8;
            }}
            
            .links {{
                text-align: center;
                margin-top: 40px;
                padding-top: 30px;
                border-top: 1px solid #eee;
            }}
            
            .btn {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 12px 30px;
                background: var(--primary-color);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                margin: 0 10px;
                transition: var(--transition);
                font-weight: bold;
                border: none;
                cursor: pointer;
                font-family: inherit;
            }}
            
            .btn:hover {{
                background: #2980b9;
                transform: translateY(-2px);
            }}
            
            .btn-secondary {{
                background: #95a5a6;
            }}
            
            .btn-secondary:hover {{
                background: #7f8c8d;
            }}
            
            .stats {{
                display: flex;
                justify-content: center;
                gap: 30px;
                margin: 30px 0;
                flex-wrap: wrap;
            }}
            
            .stat-item {{
                text-align: center;
                padding: 20px;
            }}
            
            .stat-number {{
                font-size: 2.5rem;
                font-weight: bold;
                color: var(--primary-color);
                display: block;
            }}
            
            .stat-label {{
                color: #7f8c8d;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }}
            
            /* Animações */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes countUp {{
                from {{ transform: scale(0.5); opacity: 0; }}
                to {{ transform: scale(1); opacity: 1; }}
            }}
            
            .counting {{
                animation: countUp 0.5s ease-out;
            }}
            
            /* Responsividade */
            @media (max-width: 768px) {{
                .content {{
                    padding: 20px 15px;
                }}
                
                .header {{
                    padding: 30px 20px;
                }}
                
                .grid {{
                    grid-template-columns: 1fr;
                    gap: 20px;
                }}
                
                .btn {{
                    display: flex;
                    margin: 10px auto;
                    max-width: 250px;
                    justify-content: center;
                }}
                
                .stats {{
                    gap: 15px;
                }}
                
                .stat-number {{
                    font-size: 2rem;
                }}
            }}
            
            @media (max-width: 480px) {{
                body {{
                    padding: 10px;
                }}
                
                .endpoint-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .btn {{
                    margin: 5px auto;
                }}
            }}
            
            /* Acessibilidade */
            @media (prefers-reduced-motion: reduce) {{
                * {{
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                }}
            }}
            
            /* Focus visível para acessibilidade */
            .btn:focus {{
                outline: 3px solid var(--primary-color);
                outline-offset: 2px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="badge" role="status">API v3.0</div>
                <h1>🛒 Sistema de Compra de Produtos</h1>
                <p>API para gerenciamento compra de produtos</p>
            </div>
            
            <div class="content">
                <div class="stats">
                    {stats_html}
                </div>
                
                <div class="grid">
                    {modules_html}
                </div>
                
                <div class="endpoints">
                    <h3>🔗 Endpoints Principais</h3>
                    <div class="endpoint-grid">
                        {endpoints_html}
                    </div>
                </div>
                
                <div class="links">
                    <a href="/docs" class="btn" target="_blank" rel="noopener noreferrer" aria-label="Documentação interativa da API">
                        Documentação Interativa
                    </a>
                    <a href="/redoc" class="btn btn-secondary" target="_blank" rel="noopener noreferrer" aria-label="Documentação técnica da API">
                        Documentação Técnica
                    </a>
                </div>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                // Animação melhorada para os números
                const animateValue = (element, start, end, duration, suffix = '') => {{
                    let startTimestamp = null;
                    const step = (timestamp) => {{
                        if (!startTimestamp) startTimestamp = timestamp;
                        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                        const current = Math.floor(progress * (end - start) + start);
                        element.textContent = current + suffix;
                        
                        if (progress < 1) {{
                            window.requestAnimationFrame(step);
                        }} else {{
                            element.classList.add('counting');
                        }}
                    }};
                    window.requestAnimationFrame(step);
                }};
                
                const statElements = document.querySelectorAll('.stat-number');
                
                statElements.forEach(stat => {{
                    const target = parseInt(stat.dataset.target);
                    const suffix = stat.dataset.suffix;
                    
                    // Usar Intersection Observer para animar quando o elemento estiver visível
                    const observer = new IntersectionObserver((entries) => {{
                        entries.forEach(entry => {{
                            if (entry.isIntersecting) {{
                                animateValue(stat, 0, target, 2000, suffix);
                                observer.unobserve(stat);
                            }}
                        }});
                    }}, {{ threshold: 0.5 }});
                    
                    observer.observe(stat);
                }});
                
                // Feedback visual para clicks nos botões
                document.querySelectorAll('.btn').forEach(btn => {{
                    btn.addEventListener('click', function(e) {{
                        this.style.transform = 'scale(0.95)';
                        setTimeout(() => {{
                            this.style.transform = '';
                        }}, 150);
                    }});
                }});
                
                // Adicionar classe de carregamento
                document.body.classList.add('loaded');
            }});
        </script>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Página inicial da API de E-commerce
    """
    return get_html_template()

@app.post("/auth/register")
async def register_user(username: str, email: str, password: str):
    """
    Registrar um novo usuário no sistema
    """
    return {
        "message": "Usuário registrado com sucesso",
        "user": {"username": username, "email": email}
    }

@app.post("/auth/login")
async def login_user(email: str, password: str):
    """
    Realizar login de usuário
    """
    return {
        "message": "Login realizado com sucesso",
        "user": {"email": email},
        "token": "jwt_token_exemplo"
    }

# Rotas de produtos
@app.get("/products/")
async def list_products():
    """
    Listar todos os produtos disponíveis
    """
    return {
        "products": [
            {"id": 1, "name": "Produto A", "price": 29.99},
            {"id": 2, "name": "Produto B", "price": 49.99}
        ]
    }

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """
    Obter detalhes de um produto específico
    """
    return {
        "id": product_id,
        "name": f"Produto {product_id}",
        "price": 99.99,
        "description": "Descrição do produto"
    }

@app.post("/products/")
async def create_product(name: str, price: float):
    """
    Criar um novo produto
    """
    return {
        "message": "Produto criado com sucesso",
        "product": {"name": name, "price": price}
    }

# Endpoint adicional para informações da API
@app.get("/api/info")
async def api_info():
    """Retorna informações sobre a API"""
    return {
        "name": "Sistema de E-commerce API",
        "version": "3.0",
        "description": "API completa para gerenciamento de loja virtual",
        "endpoints_count": 6,
        "modules_count": 3,
        "status": "active"
    }