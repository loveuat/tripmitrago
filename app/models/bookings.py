from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    # Trip
    trip_type = Column(String(100), nullable=False)

    # Pickup
    pickup_location_id = Column(Integer, nullable=True)
    pickup_location = Column(String(150), nullable=False)

    # Drop
    drop_location_id = Column(Integer, nullable=True)
    drop_location = Column(String(150), nullable=False)

    # Schedule
    pickup_date = Column(Date, nullable=False)
    pickup_time = Column(Time, nullable=False)

    # Vehicle
    passengers = Column(Integer, nullable=False)
    car_type = Column(String(100), nullable=False)

    # Customer
    name = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(150), nullable=False)

    # Notes
    special_instructions = Column(Text, nullable=True)

    # Booking management
    status = Column(String(50), default="pending", nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    