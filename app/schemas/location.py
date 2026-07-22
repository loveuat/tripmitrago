from pydantic import BaseModel


class LocationSearchResult(BaseModel):
    id: int
    name: str
    type: str
    state: str
    district: str | None = None
    sub_district: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    class Config:
        from_attributes = True