from sqladmin import ModelView

from app.models.location import Location
from app.models.trip_type import TripType
from app.models.bookings import Booking

class LocationAdmin(ModelView, model=Location):
    column_list = "__all__"


class TripTypeAdmin(ModelView, model=TripType):
    column_list = "__all__"

class BookingAdmin(ModelView, model=Booking):
    column_list = "__all__"

    column_searchable_list = [
        Booking.name,
        Booking.phone,
        Booking.email,
        Booking.pickup_location,
        Booking.drop_location,
]