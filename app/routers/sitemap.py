from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.location import Location
from app.models.popular_routes import PopularRoute
router = APIRouter(prefix="/api/v1/sitemap", tags=["Sitemap"])


class SitemapEntry(BaseModel):
    slug: str
    district_slug: str | None = None
    state_slug: str | None = None
    updated_at: str | None = None


class AreaSitemapEntry(BaseModel):
    slug: str
    district_slug: str | None = None
    state_slug: str | None = None


def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


@router.get("/villages", response_model=list[SitemapEntry])
def sitemap_villages(db: Session = Depends(get_db)):
    rows = (
        db.query(Location.slug, Location.district, Location.state, Location.updated_at)
        .filter(Location.is_active == True, Location.slug.isnot(None))
        .all()
    )
    return [
        SitemapEntry(
            slug=r.slug,
            district_slug=slugify(r.district) if r.district else None,
            state_slug=slugify(r.state) if r.state else None,
            updated_at=r.updated_at.isoformat() if r.updated_at else None,
        )
        for r in rows
    ]


@router.get("/districts", response_model=list[AreaSitemapEntry])
def sitemap_districts(db: Session = Depends(get_db)):
    rows = (
        db.query(Location.district, Location.state)
        .filter(Location.district.isnot(None), Location.is_active == True)
        .distinct()
        .all()
    )
    return [
        AreaSitemapEntry(slug=slugify(district), state_slug=slugify(state) if state else None)
        for district, state in rows if district
    ]


@router.get("/tehsils", response_model=list[AreaSitemapEntry])
def sitemap_tehsils(db: Session = Depends(get_db)):
    rows = (
        db.query(Location.district, Location.sub_district, Location.state)
        .filter(
            Location.district.isnot(None),
            Location.sub_district.isnot(None),
            Location.is_active == True,
        )
        .distinct()
        .all()
    )
    seen = set()
    result = []
    for district, tehsil, state in rows:
        district_slug = slugify(district)
        tehsil_slug = slugify(tehsil)
        state_slug = slugify(state) if state else None
        key = (district_slug, tehsil_slug)
        if key in seen:
            continue
        seen.add(key)
        result.append(AreaSitemapEntry(slug=tehsil_slug, district_slug=district_slug, state_slug=state_slug))
    return result

class RouteSitemapEntry(BaseModel):
    slug: str
    updated_at: str | None = None


@router.get("/routes", response_model=list[RouteSitemapEntry])
def sitemap_routes(db: Session = Depends(get_db)):
    rows = db.query(PopularRoute).all()
    result = []
    for r in rows:
        if not r.from_location or not r.to_location:
            continue
        slug = f"{slugify(r.from_location)}-to-{slugify(r.to_location)}"
        result.append(
            RouteSitemapEntry(
                slug=slug,
                updated_at=r.updated_at.isoformat() if getattr(r, "updated_at", None) else None,
            )
        )
    return result