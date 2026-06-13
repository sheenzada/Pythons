from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal

from schemas import OrderCreate, DriverCreate
from crud import (
    create_order,
    get_orders,
    create_driver,
    get_drivers
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Delivery App")


@app.get("/")
def home():
    return {"message": "Delivery API Running"}


# ---------------- ORDERS ----------------

@app.post("/orders")
def add_order(order: OrderCreate):

    db: Session = SessionLocal()

    return create_order(
        db,
        order.customer_name,
        order.pickup_location,
        order.drop_location
    )


@app.get("/orders")
def all_orders():

    db: Session = SessionLocal()

    return get_orders(db)


# ---------------- DRIVERS ----------------

@app.post("/drivers")
def add_driver(driver: DriverCreate):

    db: Session = SessionLocal()

    return create_driver(
        db,
        driver.name,
        driver.phone,
        driver.vehicle
    )


@app.get("/drivers")
def all_drivers():

    db: Session = SessionLocal()

    return get_drivers(db)