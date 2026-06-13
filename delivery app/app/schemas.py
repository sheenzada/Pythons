from pydantic import BaseModel


# ---------------- ORDERS ----------------
class OrderCreate(BaseModel):
    customer_name: str
    pickup_location: str
    drop_location: str


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    pickup_location: str
    drop_location: str
    status: str
    driver_id: int | None = None

    class Config:
        from_attributes = True


# ---------------- DRIVERS ----------------
class DriverCreate(BaseModel):
    name: str
    phone: str
    vehicle: str


class DriverResponse(BaseModel):
    id: int
    name: str
    phone: str
    vehicle: str

    class Config:
        from_attributes = True