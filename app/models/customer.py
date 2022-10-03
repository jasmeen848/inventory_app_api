from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base

from app.db.base_class import Base


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    gender = Column(TINYINT, nullable=False)
    phone_number = Column(String(15), nullable=False)
    address = Column(String(300), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)
