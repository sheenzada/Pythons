from sqlalchemy.orm import Session

from models import Order

def create_order(
    db: Session,
    customer_name: str,
    pickup_location: str,
    drop_location: str
):
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
from models import Driver

def create_driver(
    db,
    name,
    phone,
    vehicle
):
    driver = Driver(
        name=name,
        phone=phone,
        vehicle=vehicle
    )

    db.add(driver)
    db.commit()
    db.refresh(driver)

    return driver


def get_drivers(db):
    return db.query(Driver).all()