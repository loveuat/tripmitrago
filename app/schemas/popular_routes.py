from pydantic import BaseModel
from typing import Optional


class PopularRouteResponse(BaseModel):
    id: int

    image: Optional[str] = None

    from_city: str
    from_city_hi: Optional[str] = None

    to_city: str
    to_city_hi: Optional[str] = None

    price: int

    distance: str
    distance_hi: Optional[str] = None

    trip_time: str
    trip_time_hi: Optional[str] = None

    class Config:
        from_attributes = True