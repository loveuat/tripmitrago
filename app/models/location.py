from sqlalchemy import Column, Integer, String, Float, Index

from app.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    type = Column(String(50), nullable=False)

    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=True)
    sub_district = Column(String(100), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    __table_args__ = (
        Index("idx_location_name", "name"),
        Index("idx_location_state", "state"),
        Index("idx_location_district", "district"),
    )