from .auth import router as auth_router
from .products import router as products_router
from .admin import router as admin_router

from . import auth
from . import products  
from . import admin

__all__ = ["auth", "products", "admin", "auth_router", "products_router", "admin_router"]