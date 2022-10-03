from typing import Optional, Any, List

from sqlalchemy.orm import Session

from app.models.booking import Booking


class BookingDetailsRepository(Booking):

    def get_booking_by_vehicle_id(self, db: Session, vehicle_id: Any, booked_id: Any) -> Optional[Booking]:
        return db.query(Booking).filter(Booking.inventory_id == vehicle_id, Booking.booked_by == booked_id).first()

    def get_booking_by_id(self, db: Session, i_id: Any) -> Optional[Booking]:
        return db.query(Booking).filter(Booking.id == i_id).first()

    def get_booking_by_customer_id(self, db: Session, customer_id: Any) -> Optional[Booking]:
        return db.query(Booking).filter(Booking.booked_by == customer_id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Booking]:
        return db.query(Booking).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Booking) -> Booking:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in

    def update(self, db: Session, *, obj_in: Booking) -> Booking:
        db.merge(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in


booking_details_repository = BookingDetailsRepository()
