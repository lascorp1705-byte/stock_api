from sqlalchemy import Column, Integer, String
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    qty_sent = Column(Integer, default=0)
    qty_received = Column(Integer, default=0)