from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.database import Base


class PopularRoute(Base):
    __tablename__ = "popular_routes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    image = Column(
        String(255),
        nullable=True
    )

    # English
    from_city = Column(
        String(100),
        nullable=False
    )

    # Hindi
    from_city_hi = Column(
        String(100),
        nullable=True
    )

    # English
    to_city = Column(
        String(100),
        nullable=False
    )

    # Hindi
    to_city_hi = Column(
        String(100),
        nullable=True
    )

    price = Column(
        Integer,
        nullable=False
    )

    # English
    distance = Column(
        String(50),
        nullable=False
    )

    # Hindi
    distance_hi = Column(
        String(50),
        nullable=True
    )

    # English
    trip_time = Column(
        String(50),
        nullable=False
    )

    # Hindi
    trip_time_hi = Column(
        String(50),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )