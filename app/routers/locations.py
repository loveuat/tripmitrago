from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.schemas.location_detail import LocationDetail
from app.database import get_db
from app.models.location import Location
from app.schemas.location import LocationSearchResult

router = APIRouter(
    prefix="/api/v1/locations",
    tags=["Locations"]
)


@router.get(
    "/search",
    response_model=list[LocationSearchResult]
)
def search_locations(
    q: str = Query(..., min_length=2),
    lang: str = Query("en"),
    db: Session = Depends(get_db)
):
    query = (
        db.query(Location)
        .filter(Location.is_active == True)
    )

    if lang == "hi":
        query = query.filter(
            or_(
                Location.name_hi.ilike(f"%{q}%"),
                Location.name.ilike(f"%{q}%"),
            )
        )
    else:
        query = query.filter(
            or_(
                Location.name.ilike(f"%{q}%"),
                Location.name_hi.ilike(f"%{q}%"),
            )
        )

    locations = (
        query
        .order_by(
            Location.priority.desc(),
            Location.name.asc(),
        )
        .limit(10)
        .all()
    )

    return locations

@router.get(
    "/{slug}",
    response_model=LocationDetail
)
def get_location(
    slug: str,
    lang: str = Query("en"),
    db: Session = Depends(get_db)
):
    location = (
        db.query(Location)
        .filter(
            Location.slug == slug,
            Location.is_active == True
        )
        .first()
    )

    if not location:
        raise HTTPException(
            status_code=404,
            detail="Location not found"
        )

    if lang == "hi":

        if location.name_hi:
            location.name = location.name_hi

        if location.country_hi:
            location.country = location.country_hi

        if location.state_hi:
            location.state = location.state_hi

        if location.district_hi:
            location.district = location.district_hi

        if location.sub_district_hi:
            location.sub_district = location.sub_district_hi

        if location.block_hi:
            location.block = location.block_hi

        if location.panchayat_hi:
            location.panchayat = location.panchayat_hi

        if location.seo_title_hi:
            location.seo_title = location.seo_title_hi

        if location.seo_description_hi:
            location.seo_description = location.seo_description_hi

        if location.keywords_hi:
            location.keywords = location.keywords_hi

        if location.content_hi:
            location.content = location.content_hi

    return location