from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base

from app.db.base_class import Base


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True)
    vehicle_type = Column(TINYINT, nullable=False)
    vehicle_number = Column(String(50), nullable=False)
    price = Column(String(50), nullable=False)
    is_available = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)
