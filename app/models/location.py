from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    Index,
)
from sqlalchemy.sql import func

from app.database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    # ---------------------------------
    # Basic Information
    # ---------------------------------

    name = Column(String(150), nullable=False)
    name_hi = Column(String(150), nullable=True)

    type = Column(String(50), nullable=False)

    country = Column(String(100), nullable=True)
    country_hi = Column(String(100), nullable=True)

    state = Column(String(100), nullable=False)
    state_hi = Column(String(100), nullable=True)

    district = Column(String(100), nullable=True)
    district_hi = Column(String(100), nullable=True)

    sub_district = Column(String(100), nullable=True)
    sub_district_hi = Column(String(100), nullable=True)

    block = Column(String(100), nullable=True)
    block_hi = Column(String(100), nullable=True)

    panchayat = Column(String(150), nullable=True)
    panchayat_hi = Column(String(150), nullable=True)

    pincode = Column(String(10), nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    slug = Column(
        String(255),
        nullable=True,
        unique=True,
    )

    # ---------------------------------
    # Business
    # ---------------------------------

    is_serviceable = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    priority = Column(
        Integer,
        default=0,
        nullable=False,
    )

    airport_code = Column(
        String(10),
        nullable=True,
    )

    railway_station_code = Column(
        String(10),
        nullable=True,
    )

    # ---------------------------------
    # SEO
    # ---------------------------------

    seo_title = Column(
        String(255),
        nullable=True,
    )

    seo_title_hi = Column(
        String(255),
        nullable=True,
    )

    seo_description = Column(
        Text,
        nullable=True,
    )

    seo_description_hi = Column(
        Text,
        nullable=True,
    )

    keywords = Column(
        Text,
        nullable=True,
    )

    keywords_hi = Column(
        Text,
        nullable=True,
    )

    # ---------------------------------
    # AI / Dynamic Content
    # ---------------------------------

    content = Column(
        Text,
        nullable=True,
    )

    content_hi = Column(
        Text,
        nullable=True,
    )

    # ---------------------------------
    # Images
    # ---------------------------------

    banner_image = Column(
        String(255),
        nullable=True,
    )

    thumbnail_image = Column(
        String(255),
        nullable=True,
    )

    # ---------------------------------
    # Status
    # ---------------------------------

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_featured = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ---------------------------------
    # Audit
    # ---------------------------------

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

    # ---------------------------------
    # Indexes
    # ---------------------------------

    __table_args__ = (
        Index("idx_location_name", "name"),
        Index("idx_location_name_hi", "name_hi"),
        Index("idx_location_state", "state"),
        Index("idx_location_district", "district"),
        Index("idx_location_block", "block"),
        Index("idx_location_pincode", "pincode"),
        Index("idx_location_slug", "slug"),
        Index("idx_location_serviceable", "is_serviceable"),
        Index("idx_location_active", "is_active"),
        Index("idx_location_featured", "is_featured"),
    )