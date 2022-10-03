from fastapi import APIRouter, Depends

from typing import Generator, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.manage import SessionLocal
from app.repository.admin_details import admin_details_repository
from app.response_helper import create_response
from app.schemas.admin import LoginAdminRequest

router = APIRouter()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post('/login')
def create_user(
        *,
        db: Session = Depends(get_db),
        obj_in: LoginAdminRequest,
) -> Any:
    user = admin_details_repository.get_by_email_password(db, email=obj_in.email, password=obj_in.password)
    if not user:
        res = create_response(True, None, 'Incorrect email or password.', 409)
    else:
        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Admin Login successfully', 200)
    return res
