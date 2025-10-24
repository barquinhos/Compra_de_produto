from typing import List
from sqlalchemy.orm import Session

from backend.app import db_models
from backend.app.models.order import OrderCreate

def get_active_order_for_consumer(db: Session, consumer_id: int) -> db_models.Order:

    active_order = db.query(db_models.Order).filter(
        db_models.Order.con_id == consumer_id,
        db_models.Order.ord_status == db_models.OrderStatus.PENDING
    ).first()

    if not active_order:
        raise ValueError("active-order-not-found")
    
    return active_order

def submit_order_items(db: Session, consumer_id: int, payload: OrderCreate) -> db_models.Order:
    try:
        active_order = get_active_order_for_consumer(db, consumer_id)
    except ValueError:
        active_order = db_models.Order(con_id=consumer_id,
        ord_status = db_models.OrderStatus.PENDING,
        ord_total_value = 0.0
    )
        db.add(active_order)
        db.commit()
        db.refresh(active_order)
    
    total_order_value = 0.0

    for item_data in payload.items:
        product = db.get(db_models.Product, item_data.prod_id)
        if not product:
            raise ValueError(f"product-not-found:{item_data.prod_id}")
        if product.stock < item_data.quantity:

            raise ValueError(f"insufficient-stock:{item_data.prod_id}")
        product.stock -= item_data.quantity
        db.commit()
        db.refresh(product)

        order_item = db_models.OrderItem(
            ord_id=active_order.ord_id,
            prod_id=product.prod_id,
            orit_quantity=item_data.quantity,
            orit_unit_price=product.prod_price
        )
        db.add(order_item)
        product.stock -= item_data.quantity
        db.commit()
        db.refresh(product)

        total_order_value += item_data.quantity * product.prod_price

    active_order.ord_total_amount += total_order_value
    db.commit()
    db.refresh(active_order)
    
    return active_order

def get_customer_order_history(db: Session, customer_id: int) -> List[db_models.Order]:

    return db.query(db_models.Order).filter(
        db_models.Order.con_id == customer_id
    ).order_by(db_models.Order.ord_created_at.desc()).all()

def get_orders_by_status(db: Session, status: str) -> List[db_models.Order]:

    return db.query(db_models.Order).filter(
        db_models.Order.ord_status == status
    ).all()