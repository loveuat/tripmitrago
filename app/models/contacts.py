from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    consent = Column(Boolean, nullable=False, default=False)
    newscheckbox = Column(Boolean, nullable=False, default=False)

    status = Column(String, default="new")

    status = Column(String(20), default="new", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())