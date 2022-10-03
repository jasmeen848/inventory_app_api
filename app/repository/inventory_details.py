from typing import Optional, Any, List
from sqlalchemy.orm import Session

from sqlalchemy import Integer, func
from app.models.inventory import Inventory


class InventoryDetailsRepository(Inventory):

    def get_inventory_by_vehicle_id(self, db: Session, vehicle_id: Any) -> Optional[Inventory]:
        return db.query(Inventory).filter(Inventory.vehicle_number == vehicle_id).first()

    def get_inventory_by_id(self, db: Session, i_id: Any) -> Optional[Inventory]:
        return db.query(Inventory).filter(Inventory.id == i_id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Inventory]:
        return db.query(Inventory).offset(skip).limit(limit).all()

    def get_by_email(self, db: Session, *, email: str) -> Optional[Inventory]:
        return db.query(Inventory).filter(Inventory.email == email).first()

    def create(self, db: Session, *, obj_in: Inventory) -> Inventory:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session, *, obj_in: Inventory) -> Inventory:
        db.merge(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def get_bike(self, db: Session) -> Integer:
        query = db.query(func.count(Inventory.vehicle_type)).filter(Inventory.vehicle_type == 1, Inventory.is_available == True)
        return query.scalar()

    def get_car(self, db: Session) -> Integer:
        query = db.query(func.count(Inventory.vehicle_type)).filter(Inventory.vehicle_type == 3, Inventory.is_available == True)
        return query.scalar()

    def get_cycle(self, db: Session) -> Integer:
        query = db.query(func.count(Inventory.vehicle_type)).filter(Inventory.vehicle_type == 2, Inventory.is_available == True)
        return query.scalar()

    def get_boat(self, db: Session) -> Integer:
        query = db.query(func.count(Inventory.vehicle_type)).filter(Inventory.vehicle_type == 4, Inventory.is_available == True)
        return query.scalar()

inventory_details_repository = InventoryDetailsRepository()
