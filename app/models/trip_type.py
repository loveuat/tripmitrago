from sqlalchemy import Column, Integer, String, Boolean, Text

from app.database import Base
class TripType(Base):
    __tablename__ = "trip_types"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    sort_order = Column(Integer, default=0, nullable=False)