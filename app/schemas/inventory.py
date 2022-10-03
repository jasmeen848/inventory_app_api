from pydantic import BaseModel
from datetime import datetime


class InventoryRequest(BaseModel):
    vehicle_type: int
    price: str
    vehicle_number: str
    is_available: bool
    is_active: bool


class EditInventoryRequest(BaseModel):
    id: int
    is_available: bool
    is_active: bool


class InventoryResponse(BaseModel):
    id: int
    vehicle_type: int
    price: str
    vehicle_number: str
    is_available: bool
    is_active: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
        orm_mode = True
