from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

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
    db: Session = Depends(get_db)
):
    locations = (
        db.query(Location)
        .filter(Location.name.ilike(f"%{q}%"))
        .order_by(Location.name)
        .limit(10)
        .all()
    )

    return locations