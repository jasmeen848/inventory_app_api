from datetime import datetime

from fastapi import APIRouter, Depends

from typing import Generator, List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.manage import SessionLocal
from app.models.booking import Booking
from app.repository.booking_details import booking_details_repository
from app.response_helper import create_response
from app.schemas.booking import BookingRequest, BookingResponse, EditBookingRequest

router = APIRouter()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/booking', response_model=List[BookingResponse])
def get_all_booking(
        db: Session = Depends(get_db),
) -> Any:
    users = booking_details_repository.get_multi(db)

    if len(users) > 0:
        json_compatible_item_data = jsonable_encoder(users)
        res = create_response(False, json_compatible_item_data, 'list of all bookings.', 200)
    else:
        res = create_response(
            True,
            [],
            "No data found.",
            204
        )
    return res


@router.get('/booking/{customer_id}', response_model=List[BookingResponse])
def get_all_booking(
        customer_id: int,
        db: Session = Depends(get_db),
) -> Any:
    user = booking_details_repository.get_booking_by_customer_id(db, customer_id=customer_id)

    if user:
        json_compatible_item_data = jsonable_encoder(user)
        res = create_response(False, json_compatible_item_data, 'booking details found.', 200)
    else:
        res = create_response(
            False,
            {},
            "No data found.",
            204
        )
    return res

@router.post('/booking')
def create_booking(
        *,
        db: Session = Depends(get_db),
        obj_in: BookingRequest,
) -> Any:
    user = booking_details_repository.get_booking_by_vehicle_id(db, vehicle_id=obj_in.inventory_id, booked_id=obj_in.booked_by)
    if user:
        res = create_response(True, user.id, 'Booking already exists in the system.', 409)

    else:
        obj = Booking()
        obj.inventory_id = obj_in.inventory_id
        obj.booked_by = obj_in.booked_by
        obj.booking_on = obj_in.booking_on
        obj.start_from = obj_in.start_from
        obj.return_on = obj_in.return_on
        obj.is_submitted = False
        obj.is_paid = obj_in.is_paid
        obj.is_active = obj_in.is_active
        obj.created_on = datetime.now()
        obj.updated_on = datetime.now()
        user = booking_details_repository.create(db, obj_in=obj)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Booking successful', 200)
    return res


@router.put('/booking')
def update_booking(
        *,
        db: Session = Depends(get_db),
        obj_in: EditBookingRequest,
) -> Any:
    user = booking_details_repository.get_booking_by_id(db, i_id=obj_in.id)
    if not user:
        res = create_response(True, None, 'Booking does not exist in the system.', 422)

    else:
        user.is_paid = obj_in.is_paid
        user.is_submitted = obj_in.is_submitted
        user.is_active = obj_in.is_active
        user.updated_on = datetime.now()
        user = booking_details_repository.update(db, obj_in=user)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Booking updated successfully', 201)
    return res



