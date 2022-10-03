from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMTEXT

from app.db.base_class import Base


class Booking(Base):
    __tablename__ = 'booking-details'

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, nullable=False)
    booked_by = Column(Integer, nullable=False)
    booking_on = Column(DateTime, nullable=False)
    start_from = Column(DateTime, nullable=False)
    return_on = Column(DateTime, nullable=False)
    is_paid = Column(Boolean, nullable=False, default=False)
    is_submitted = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)
