from pydantic import BaseModel
from datetime import datetime


class BookingRequest(BaseModel):
    inventory_id: int
    booked_by: int
    booking_on: datetime
    start_from: datetime
    return_on: datetime
    is_paid: bool
    is_active: bool


class EditBookingRequest(BaseModel):
    id: int
    is_submitted: bool
    is_paid: bool
    is_active: bool


class BookingResponse(BaseModel):
    id: int
    inventory_id: int
    booked_by: int
    booking_on: datetime
    start_from: datetime
    return_on: datetime
    is_submitted: bool
    is_paid: bool
    is_active: bool
    created_on: datetime
    updated_on: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
        }
        orm_mode = True
