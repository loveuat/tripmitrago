from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func

from app.database import Base


class AreaBanner(Base):
    """
    District/Tehsil don't have their own DB rows (they're just column
    values on Location), so this small table lets admins attach a
    banner image to a district or tehsil by name, without needing
    the full Location schema.
    """
    __tablename__ = "area_banners"

    id = Column(Integer, primary_key=True, index=True)

    level = Column(String(20), nullable=False)  # "district" or "tehsil"

    # Slugs are computed the same way as the frontend/backend slugify()
    slug = Column(String(150), nullable=False)          # e.g. "kukshi"
    district_slug = Column(String(150), nullable=True)   # only for level="tehsil", disambiguates same-name tehsils across districts

    name = Column(String(150), nullable=False)  # display name, e.g. "Kukshi"
    state = Column(String(100), nullable=True)

    banner_image = Column(String(500), nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("idx_area_banner_level_slug", "level", "slug", "district_slug"),
    )