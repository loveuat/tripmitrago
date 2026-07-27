from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.popular_routes import PopularRoute
from app.schemas.popular_routes import PopularRouteResponse


router = APIRouter(
    prefix="/api/v1/popular-routes",
    tags=["Popular Routes"]
)


@router.get(
    "",
    response_model=list[PopularRouteResponse]
)
def get_popular_routes(
    db: Session = Depends(get_db)
):

    routes = (
        db.query(PopularRoute)
        .order_by(PopularRoute.id.desc())
        .all()
    )

    return routes