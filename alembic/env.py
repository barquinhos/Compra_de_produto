import logging.config
fileConfig = logging.config.fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, '..', 'compra_de_produtos', 'backend')
sys.path.insert(0, os.path.abspath(backend_path))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# from app.database.session import Base
# from app.models.user import User
# from app.models.product import Product, Category
# from app.models.order import Cart, CartItem, Order, OrderItem

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    print("Offline mode not supported")
else:
    run_migrations_online()