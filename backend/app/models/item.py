from sqlalchemy import Column, Float, Integer, String, Text

from app.core.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    size = Column(String, nullable=False)
    color = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    front_image_path = Column(String, nullable=False)
    back_image_path = Column(String, nullable=False)