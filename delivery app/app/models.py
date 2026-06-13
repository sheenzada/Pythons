from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String)
    pickup_location = Column(String)
    drop_location = Column(String)

    status = Column(
        String,
        default="Pending"
    )


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    phone = Column(String)
    vehicle = Column(String)