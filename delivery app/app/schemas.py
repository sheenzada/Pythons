from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_name: str
    pickup_location: str
    drop_location: str

class OrderResponse(OrderCreate):
    id: int
    status: str

    class Config:
        from_attributes = True
from pydantic import BaseModel

class DriverCreate(BaseModel):
    name: str
    phone: str
    vehicle: str


class DriverResponse(DriverCreate):
    id: int

    class Config:
        from_attributes = True