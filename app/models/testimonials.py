from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func

from app.database import Base


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    name_hi = Column(String(100), nullable=True)

    designation = Column(String(150), nullable=False)
    designation_hi = Column(String(150), nullable=True)

    content = Column(Text, nullable=False)
    content_hi = Column(Text, nullable=True)

    rating = Column(Float, default=4.5, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )