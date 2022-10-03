from pydantic import BaseModel
from datetime import datetime


class CustomerRequest(BaseModel):
    name: str
    gender: int
    email: str
    address: str
    phone_number: str
    is_active: bool


class EditCustomerRequest(BaseModel):
    id: int
    name: str
    gender: int
    email: str
    address: str
    phone_number: str
    is_active: bool


class DeleteCustomerRequest(BaseModel):
    id: int
    is_active: bool


class CustomerResponse(BaseModel):
    id: int
    name: str
    gender: int
    email: str
    address: str
    phone_number: str
    is_active: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
        orm_mode = True
