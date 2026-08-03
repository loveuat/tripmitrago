from fastapi import APIRouter, Depends, Query
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
    lang: str = Query("en"),
    db: Session = Depends(get_db)
):

    routes = (
        db.query(PopularRoute)
        .order_by(PopularRoute.id.desc())
        .all()
    )

    response = []

    for route in routes:
        response.append(
            PopularRouteResponse(
                id=route.id,
                image=route.image,

                from_city=(
                    route.from_city_hi
                    if lang == "hi" and route.from_city_hi
                    else route.from_city
                ),

                to_city=(
                    route.to_city_hi
                    if lang == "hi" and route.to_city_hi
                    else route.to_city
                ),

                price=route.price,

                distance=(
                    route.distance_hi
                    if lang == "hi" and route.distance_hi
                    else route.distance
                ),

                trip_time=(
                    route.trip_time_hi
                    if lang == "hi" and route.trip_time_hi
                    else route.trip_time
                ),

                # Optional (schema me agar fields hain)
                from_city_hi=route.from_city_hi,
                to_city_hi=route.to_city_hi,
                distance_hi=route.distance_hi,
                trip_time_hi=route.trip_time_hi,
            )
        )

    return response