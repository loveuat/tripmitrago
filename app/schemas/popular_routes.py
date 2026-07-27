from pydantic import BaseModel


class PopularRouteResponse(BaseModel):
    id: int
    image: str | None = None
    from_city: str
    to_city: str
    price: int
    distance: str
    trip_time: str

    class Config:
        from_attributes = True