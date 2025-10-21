from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import db_models
from ..models.cart import CartItemCreate, CartItemUpdate

class CartService:
    
    def get_or_create_cart(self, db: Session, consumer_id: int) -> db_models.Cart:
        cart = db.query(db_models.Cart).filter(db_models.Cart.con_id == consumer_id).first()
        
        if not cart:
            cart = db_models.Cart(con_id=consumer_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        
        return cart

    def add_item_to_cart(self, db: Session, consumer_id: int, item_data: CartItemCreate) -> db_models.Cart:
        product = db.query(db_models.Product).filter(
            db_models.Product.prod_id == item_data.product_id
        ).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        if product.stock < item_data.quantity:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        
        cart = self.get_or_create_cart(db, consumer_id)
        
        existing_item = db.query(db_models.CartItem).filter(
            db_models.CartItem.cart_id == cart.car_id,
            db_models.CartItem.product_id == item_data.product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += item_data.quantity
            if product.stock < existing_item.quantity:
                raise HTTPException(status_code=400, detail="Estoque insuficiente")
        else:
            new_item = db_models.CartItem(
                cart_id=cart.car_id,
                product_id=item_data.product_id,
                quantity=item_data.quantity
            )
            db.add(new_item)
        
        db.commit()
        db.refresh(cart)
        return cart

    def update_cart_item(self, db: Session, consumer_id: int, item_id: int, item_data: CartItemUpdate) -> db_models.Cart:
        cart = self.get_or_create_cart(db, consumer_id)
        
        cart_item = db.query(db_models.CartItem).filter(
            db_models.CartItem.carit_id == item_id,
            db_models.CartItem.cart_id == cart.car_id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        if cart_item.product.stock < item_data.quantity:
            raise HTTPException(status_code=400, detail="Estoque insuficiente")
        
        cart_item.quantity = item_data.quantity
        db.commit()
        db.refresh(cart)
        return cart

    def remove_item_from_cart(self, db: Session, consumer_id: int, item_id: int) -> db_models.Cart:
        cart = self.get_or_create_cart(db, consumer_id)
        
        cart_item = db.query(db_models.CartItem).filter(
            db_models.CartItem.carit_id == item_id,
            db_models.CartItem.cart_id == cart.car_id
        ).first()
        
        if not cart_item:
            raise HTTPException(status_code=404, detail="Item não encontrado")
        
        db.delete(cart_item)
        db.commit()
        db.refresh(cart)
        return cart

    def clear_cart(self, db: Session, consumer_id: int) -> dict:
        cart = self.get_or_create_cart(db, consumer_id)
        
        db.query(db_models.CartItem).filter(db_models.CartItem.cart_id == cart.car_id).delete()
        db.commit()
        
        return {"message": "Carrinho limpo"}

cart_service = CartService()