from typing import Optional, Any, List
from sqlalchemy.orm import Session

from app.models.admin import Admin


class AdminDetailsRepository(Admin):

    def get_user_by_id(self, db: Session, customer_id: Any) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.id == customer_id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Admin]:
        return db.query(Admin).offset(skip).limit(limit).all()

    def get_by_email(self, db: Session, *, email: str) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.email == email).first()

    def get_by_email_password(self, db: Session, *, email: str, password: str) -> Optional[Admin]:
        return db.query(Admin).filter(Admin.email == email, Admin.password == password).first()

    def create(self, db: Session, *, obj_in: Admin) -> Admin:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session, *, obj_in: Admin) -> Admin:
        db.merge(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in


admin_details_repository = AdminDetailsRepository()
