from datetime import datetime

from fastapi import APIRouter, Depends

from typing import Generator, List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.manage import SessionLocal
from app.models.admin import Admin
from app.repository.admin_details import admin_details_repository
from app.response_helper import create_response
from app.schemas.admin import AdminResponse, AdminRequest, EditAdminRequest

router = APIRouter()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/admin', response_model=List[AdminResponse])
def get_all_users(
        db: Session = Depends(get_db),
) -> Any:
    users = admin_details_repository.get_multi(db)

    if len(users) > 0:
        json_compatible_item_data = jsonable_encoder(users)
        res = create_response(False, json_compatible_item_data, 'list of all Admin.', 200)
    else:
        res = create_response(
            True,
            [],
            "No data found.",
            204
        )
    return res


@router.get('/admin/{user_id}', response_model=AdminResponse)
def get_users(
        user_id: int,
        db: Session = Depends(get_db),
) -> Any:
    user = admin_details_repository.get_user_by_id(db, customer_id=user_id)

    if user:
        json_compatible_item_data = jsonable_encoder(user)
        res = create_response(False, json_compatible_item_data, 'Admin details found.', 200)
    else:
        res = create_response(
            False,
            {},
            "No data found.",
            204
        )
    return res


@router.post('/admin')
def create_user(
        *,
        db: Session = Depends(get_db),
        obj_in: AdminRequest,
) -> Any:
    user = admin_details_repository.get_by_email(db, email=obj_in.email)
    if user:
        res = create_response(True, user.id, 'Admin already exists in the system.', 409)

    else:
        obj = Admin()
        obj.name = obj_in.name
        obj.email = obj_in.email
        obj.password = obj_in.password
        obj.is_active = obj_in.is_active
        obj.created_on = datetime.now()
        obj.updated_on = datetime.now()
        user = admin_details_repository.create(db, obj_in=obj)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Admin Created successfully', 200)
    return res


@router.put('/admin')
def update_user(
        *,
        db: Session = Depends(get_db),
        obj_in: EditAdminRequest,
) -> Any:
    user = admin_details_repository.get_user_by_id(db, customer_id=obj_in.id)

    if not user:
        res = create_response(True, None, 'Admin does not exist in the system.', 422)

    else:
        user.password = obj_in.password
        user.is_active = obj_in.is_active
        user.updated_on = datetime.now()
        user = admin_details_repository.update(db, obj_in=user)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Admin updated successfully', 201)
    return res
