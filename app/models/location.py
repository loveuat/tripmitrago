from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Index,
)
from sqlalchemy.sql import func

from app.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    # Existing
    name = Column(String(150), nullable=False)
    type = Column(String(50), nullable=False)

    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=True)
    sub_district = Column(String(100), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # New
    country = Column(String(100), nullable=True)
    block = Column(String(100), nullable=True)
    panchayat = Column(String(150), nullable=True)
    pincode = Column(String(10), nullable=True)

    slug = Column(String(255), nullable=True, unique=True)

    is_serviceable = Column(Boolean, default=False, nullable=False)
    priority = Column(Integer, default=0, nullable=False)

    airport_code = Column(String(10), nullable=True)
    railway_station_code = Column(String(10), nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_location_name", "name"),
        Index("idx_location_state", "state"),
        Index("idx_location_district", "district"),
        Index("idx_location_block", "block"),
        Index("idx_location_pincode", "pincode"),
        Index("idx_location_serviceable", "is_serviceable"),
    )