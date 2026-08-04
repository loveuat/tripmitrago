from pydantic import BaseModel


class LocationDetail(BaseModel):
    id: int

    name: str
    type: str

    country: str | None = None
    state: str
    district: str | None = None
    sub_district: str | None = None
    block: str | None = None
    panchayat: str | None = None

    pincode: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    slug: str

    is_serviceable: bool
    priority: int

    airport_code: str | None = None
    railway_station_code: str | None = None

    seo_title: str | None = None
    seo_description: str | None = None
    keywords: str | None = None

    content: str | None = None

    banner_image: str | None = None
    thumbnail_image: str | None = None

    is_active: bool
    is_featured: bool

    class Config:
        from_attributes = True