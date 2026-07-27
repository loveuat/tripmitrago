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

    from_city = Column(
        String(100),
        nullable=False
    )

    to_city = Column(
        String(100),
        nullable=False
    )

    price = Column(
        Integer,
        nullable=False
    )

    distance = Column(
        String(50),
        nullable=False
    )

    trip_time = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )