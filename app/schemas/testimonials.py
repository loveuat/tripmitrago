from datetime import datetime
from pydantic import BaseModel


class TestimonialResponse(BaseModel):
    id: int
    name: str
    designation: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True