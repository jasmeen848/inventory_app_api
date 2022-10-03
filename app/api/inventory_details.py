from datetime import datetime

from fastapi import APIRouter, Depends

from typing import Generator, List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.manage import SessionLocal
from app.models.inventory import Inventory
from app.repository.inventory_details import inventory_details_repository
from app.response_helper import create_response
from app.schemas.inventory import InventoryResponse, InventoryRequest, EditInventoryRequest

router = APIRouter()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/inventory', response_model=List[InventoryResponse])
def get_all_inventory(
        db: Session = Depends(get_db),
) -> Any:
    users = inventory_details_repository.get_multi(db)
    car_total = inventory_details_repository.get_car(db)
    cycle_total = inventory_details_repository.get_cycle(db)
    bike_total = inventory_details_repository.get_bike(db)
    boat_total = inventory_details_repository.get_boat(db)

    if len(users) > 0:
        json_compatible_item_data = {
            'data': jsonable_encoder(users),
            'car_total': car_total,
            'cycle_total': cycle_total,
            'bike_total': bike_total,
            'boat_total': boat_total
        }
        res = create_response(False, json_compatible_item_data, 'list of all vehicles.', 200)
    else:
        res = create_response(
            True,
            [],
            "No data found.",
            204
        )
    return res


@router.post('/inventory')
def create_inventory(
        *,
        db: Session = Depends(get_db),
        obj_in: InventoryRequest,
) -> Any:
    user = inventory_details_repository.get_inventory_by_vehicle_id(db, vehicle_id=obj_in.vehicle_number)
    if user:
        res = create_response(True, user.id, 'Vehicle already exists in the system.', 409)

    else:
        obj = Inventory()
        obj.vehicle_type = obj_in.vehicle_type
        obj.price = obj_in.price
        obj.vehicle_number = obj_in.vehicle_number
        obj.is_available = obj_in.is_available
        obj.is_active = obj_in.is_active
        obj.created_on = datetime.now()
        obj.updated_on = datetime.now()
        user = inventory_details_repository.create(db, obj_in=obj)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Vehicle created successfully', 200)
    return res


@router.put('/inventory')
def update_inventory(
        *,
        db: Session = Depends(get_db),
        obj_in: EditInventoryRequest,
) -> Any:
    user = inventory_details_repository.get_inventory_by_id(db, i_id=obj_in.id)
    if not user:
        res = create_response(True, None, 'Vehicle does not exist in the system.', 422)

    else:
        user.id = obj_in.id
        user.is_available = obj_in.is_available
        user.is_active = obj_in.is_active
        user.updated_on = datetime.now()
        user = inventory_details_repository.create(db, obj_in=user)

        user_details_response = jsonable_encoder(user)
        res = create_response(False, user_details_response, 'Vehicle updated successfully', 201)
    return res



