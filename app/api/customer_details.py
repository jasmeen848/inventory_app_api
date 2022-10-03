from datetime import datetime

from fastapi import APIRouter, Depends

from typing import Generator, List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.manage import SessionLocal
from app.models.customer import Customer
from app.repository.booking_details import booking_details_repository
from app.repository.customer_details import customer_details_repository
from app.response_helper import create_response
from app.schemas.customer import CustomerResponse, CustomerRequest, EditCustomerRequest, DeleteCustomerRequest

router = APIRouter()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/customers', response_model=List[CustomerResponse])
def get_all_users(
        db: Session = Depends(get_db),
) -> Any:
    users = customer_details_repository.get_multi(db)

    if len(users) > 0:
        json_compatible_item_data = jsonable_encoder(users)
        res = create_response(False, json_compatible_item_data, 'list of all Customer.', 200)
    else:
        res = create_response(
            True,
            [],
            "No data found.",
            204
        )
    return res


@router.get('/customer/{user_id}', response_model=CustomerResponse)
def get_users(
        user_id: int,
        db: Session = Depends(get_db),
) -> Any:
    user = customer_details_repository.get_user_by_id(db, customer_id=user_id)

    if user:
        json_compatible_item_data = jsonable_encoder(user)
        res = create_response(False, json_compatible_item_data, 'Customer details found.', 200)
    else:
        res = create_response(
            False,
            {},
            "No data found.",
            204
        )
    return res


@router.post('/customer')
def create_user(
        *,
        db: Session = Depends(get_db),
        obj_in: CustomerRequest,
) -> Any:
    user = customer_details_repository.get_by_email(db, email=obj_in.email)
    if user:
        res = create_response(True, user.id, 'Customer already exists in the system.', 409)

    else:
        obj = Customer()
        obj.name = obj_in.name
        obj.gender = obj_in.gender
        obj.address = obj_in.address
        obj.email = obj_in.email
        obj.phone_number = obj_in.phone_number
        obj.is_active = obj_in.is_active
        obj.created_on = datetime.now()
        obj.updated_on = datetime.now()
        user = customer_details_repository.create(db, obj_in=obj)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Customer created successfully', 200)
    return res


@router.put('/customer')
def update_user(
        *,
        db: Session = Depends(get_db),
        obj_in: EditCustomerRequest,
) -> Any:
    user = customer_details_repository.get_user_by_id(db, customer_id=obj_in.id)

    if not user:
        res = create_response(True, None, 'Customer does not exist in the system.', 422)

    else:
        user.name = obj_in.name
        user.gender = obj_in.gender
        user.address = obj_in.address
        user.email = obj_in.email
        user.phone_number = obj_in.phone_number
        user.is_active = obj_in.is_active
        user.updated_on = datetime.now()
        user = customer_details_repository.update(db, obj_in=user)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Customer updated successfully', 201)
    return res


@router.delete('/customer')
def delete_user(
        *,
        db: Session = Depends(get_db),
        obj_in: DeleteCustomerRequest,
) -> Any:
    user = customer_details_repository.get_user_by_id(db, customer_id=obj_in.id)

    if not user:
        res = create_response(True, None, 'Customer does not exist in the system.', 422)

    else:
        booking_response = booking_details_repository.get_booking_by_customer_id(db, customer_id=user.id)

        if not booking_response:
            user.id = obj_in.id
            user.is_active = False
            user.updated_on = datetime.now()
            user = customer_details_repository.update(db, obj_in=user)

            res = create_response(False, user.id, 'Customer deleted successfully', 201)
        else:
            res = create_response(True, user.id, 'Booking exists for this customer', 422)

    return res
