from  sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from config.db import Base

#El modelo se hizo en base a los requerimientos del correo
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(300), nullable=False)
    price = Column(Float, nullable=False)
    available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), on_update=func.now())

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name}, price={self.price})>"