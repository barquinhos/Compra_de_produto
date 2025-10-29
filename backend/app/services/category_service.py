from sqlalchemy.orm import Session
from db_models import Category

def get_or_create_categories(db: Session):
    categories_data = [
        {"name": "CATEGORY_A", "description": "Categoria A"},
        {"name": "CATEGORY_B", "description": "Categoria B"},
        {"name": "CATEGORY_C", "description": "Categoria C"},
    ]
    
    for cat_data in categories_data:
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
    
    db.commit()