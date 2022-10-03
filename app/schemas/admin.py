from pydantic import BaseModel
from datetime import datetime


class AdminRequest(BaseModel):
    name: str
    email: str
    password: str
    is_active: bool


class LoginAdminRequest(BaseModel):
    email: str
    password: str


class EditAdminRequest(BaseModel):
    id: int
    password: str
    is_active: bool


class AdminResponse(BaseModel):
    id: int
    name: str
    email: str
    password: str
    is_active: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
        orm_mode = True
