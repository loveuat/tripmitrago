from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    Time,
)
from sqlalchemy.sql import func

from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Booking Reference
    booking_number = Column(String(30), unique=True, index=True, nullable=True)

    # Trip Details
    trip_type = Column(String(100), nullable=False)

    # Pickup
    pickup_location_id = Column(Integer, nullable=True, index=True)
    pickup_location = Column(String(150), nullable=False)

    # Drop
    drop_location_id = Column(Integer, nullable=True, index=True)
    drop_location = Column(String(150), nullable=False)

    # Journey
    pickup_date = Column(Date, nullable=False)
    pickup_time = Column(Time, nullable=True)

    # Vehicle
    passengers = Column(Integer, nullable=False)
    car_type = Column(String(100), nullable=True)

    # Pricing
    estimated_distance = Column(Float, nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # minutes
    estimated_fare = Column(Float, nullable=True)
    final_fare = Column(Float, nullable=True)

    # Customer
    name = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=False, index=True)
    email = Column(String(150), nullable=False, index=True)

    # Notes
    special_instructions = Column(Text, nullable=True)

    # Booking Status
    status = Column(
        String(50),
        default="pending",
        nullable=False,
        index=True,
    )

    # Payment
    payment_status = Column(String(50),nullable=False,default="pending",server_default="pending")

    payment_method = Column(String(50), nullable=True)

    # Driver
    driver_id = Column(Integer, nullable=True)
    vehicle_id = Column(Integer, nullable=True)

    # Soft Delete
    is_active = Column(Boolean, default=True, nullable=False)

    # Audit
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )