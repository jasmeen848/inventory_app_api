from typing import Optional, Any, List
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerDetailsRepository(Customer):

    def get_user_by_id(self, db: Session, customer_id: Any) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.id == customer_id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Customer]:
        return db.query(Customer).offset(skip).limit(limit).all()

    def get_by_email(self, db: Session, *, email: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.email == email).first()

    def create(self, db: Session, *, obj_in: Customer) -> Customer:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session, *, obj_in: Customer) -> Customer:
        db.merge(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in


customer_details_repository = CustomerDetailsRepository()
