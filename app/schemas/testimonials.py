from pydantic import BaseModel
from typing import Optional


class TestimonialResponse(BaseModel):
    id: int

    name: str
    name_hi: Optional[str] = None

    designation: str
    designation_hi: Optional[str] = None

    content: str
    content_hi: Optional[str] = None

    rating: float

    class Config:
        from_attributes = True