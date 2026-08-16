from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.location import Location
from app.models.area_banner import AreaBanner
from app.schemas.location import LocationSearchItem

router = APIRouter(prefix="/api/v1/areas", tags=["Areas"])


def slugify(text: str) -> str:
    import re
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


class DistrictDetail(BaseModel):
    name: str
    slug: str
    state: str
    village_count: int
    banner_image: str | None = None
    villages: list[LocationSearchItem]


class TehsilDetail(BaseModel):
    name: str
    slug: str
    district: str
    district_slug: str
    state: str
    village_count: int
    banner_image: str | None = None
    villages: list[LocationSearchItem]


def _loc_field(row, field, lang):
    hi_val = getattr(row, f"{field}_hi", None)
    return hi_val if (lang == "hi" and hi_val) else getattr(row, field, None)


def _to_item(row, lang):
    hierarchy = [h for h in [
        _loc_field(row, "sub_district", lang),
        _loc_field(row, "district", lang),
        _loc_field(row, "state", lang),
    ] if h]
    return LocationSearchItem(
        id=str(row.id),
        type=row.type,
        name=_loc_field(row, "name", lang),
        name_hi=row.name_hi,
        hierarchy=hierarchy,
        slug=row.slug,
        pincode=row.pincode,
        latitude=row.latitude,
        longitude=row.longitude,
        is_serviceable=row.is_serviceable,
        priority=row.priority,
    )


@router.get("/district/{district_slug}", response_model=DistrictDetail)
def get_district(district_slug: str, lang: str = Query("en"), db: Session = Depends(get_db)):
    districts = db.query(Location.district, Location.state).distinct().all()
    match = next((d for d in districts if d[0] and slugify(d[0]) == district_slug), None)
    if not match:
        raise HTTPException(status_code=404, detail="District not found")

    district_name, state_name = match
    rows = (
        db.query(Location)
        .filter(Location.district == district_name, Location.is_active == True)
        .order_by(Location.priority.desc(), Location.name.asc())
        .all()
    )

    banner = (
        db.query(AreaBanner)
        .filter(AreaBanner.level == "district", AreaBanner.slug == district_slug)
        .first()
    )

    return DistrictDetail(
        name=district_name,
        slug=district_slug,
        state=state_name,
        village_count=len(rows),
        banner_image=banner.banner_image if banner else None,
        villages=[_to_item(r, lang) for r in rows],
    )


@router.get("/district/{district_slug}/tehsil/{tehsil_slug}", response_model=TehsilDetail)
def get_tehsil(district_slug: str, tehsil_slug: str, lang: str = Query("en"), db: Session = Depends(get_db)):
    districts = db.query(Location.district, Location.state).distinct().all()
    dmatch = next((d for d in districts if d[0] and slugify(d[0]) == district_slug), None)
    if not dmatch:
        raise HTTPException(status_code=404, detail="District not found")
    district_name, state_name = dmatch

    tehsils = (
        db.query(Location.sub_district)
        .filter(Location.district == district_name)
        .distinct()
        .all()
    )
    tmatch = next((t[0] for t in tehsils if t[0] and slugify(t[0]) == tehsil_slug), None)
    if not tmatch:
        raise HTTPException(status_code=404, detail="Tehsil not found")

    rows = (
        db.query(Location)
        .filter(
            Location.district == district_name,
            Location.sub_district == tmatch,
            Location.is_active == True,
        )
        .order_by(Location.priority.desc(), Location.name.asc())
        .all()
    )

    banner = (
        db.query(AreaBanner)
        .filter(
            AreaBanner.level == "tehsil",
            AreaBanner.slug == tehsil_slug,
            AreaBanner.district_slug == district_slug,
        )
        .first()
    )

    return TehsilDetail(
        name=tmatch,
        slug=tehsil_slug,
        district=district_name,
        district_slug=district_slug,
        state=state_name,
        village_count=len(rows),
        banner_image=banner.banner_image if banner else None,
        villages=[_to_item(r, lang) for r in rows],
    )