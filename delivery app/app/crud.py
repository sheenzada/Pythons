from sqlalchemy.orm import Session
from app.models import Order, Driver


# ---------------- ORDERS ----------------

def create_order(db: Session, customer_name, pickup_location, drop_location):
    order = Order(
        customer_name=customer_name,
        pickup_location=pickup_location,
        drop_location=drop_location
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session):
    return db.query(Order).all()


# ---------------- DRIVERS ----------------

def create_driver(db: Session, name, phone, vehicle):
    driver = Driver(
        name=name,
        phone=phone,
        vehicle=vehicle
    )
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver


def get_drivers(db: Session):
    return db.query(Driver).all()