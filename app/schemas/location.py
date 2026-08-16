from pydantic import BaseModel


class LocationSearchResult(BaseModel):
    id: int
    # Basic
    name: str
    name_hi: str | None = None
    type: str
    country: str | None = None
    country_hi: str | None = None
    state: str
    state_hi: str | None = None
    district: str | None = None
    district_hi: str | None = None
    sub_district: str | None = None
    sub_district_hi: str | None = None
    block: str | None = None
    block_hi: str | None = None
    panchayat: str | None = None
    panchayat_hi: str | None = None
    pincode: str | None = None
    # Location
    latitude: float | None = None
    longitude: float | None = None
    slug: str | None = None
    # Business
    is_serviceable: bool
    priority: int
    airport_code: str | None = None
    railway_station_code: str | None = None
    # SEO
    seo_title: str | None = None
    seo_title_hi: str | None = None
    seo_description: str | None = None
    seo_description_hi: str | None = None
    keywords: str | None = None
    keywords_hi: str | None = None
    # Content
    content: str | None = None
    content_hi: str | None = None
    # Images
    banner_image: str | None = None
    thumbnail_image: str | None = None
    # Status
    is_active: bool
    is_featured: bool

    class Config:
        from_attributes = True


class LocationSearchItem(BaseModel):
    """
    Lightweight, index-agnostic search result.
    Shape maps 1:1 to a future Elasticsearch/OpenSearch document —
    migrating later means swapping the query function, not this contract.
    """
    id: str
    type: str
    name: str
    name_hi: str | None = None
    hierarchy: list[str] = []
    slug: str | None = None
    pincode: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_serviceable: bool = False
    priority: int = 0

    class Config:
        from_attributes = True