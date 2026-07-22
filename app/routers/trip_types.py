from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trip_type import TripType

router = APIRouter(
    prefix="/api/v1/trip-types",
    tags=["Trip Types"]
)


@router.get("")
def get_trip_types(
    db: Session = Depends(get_db)
):
    return (
        db.query(TripType)
        .filter(TripType.is_active == True)
        .order_by(TripType.sort_order.asc())
        .all()
    )