from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.base_class import Base


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime, nullable=False)
