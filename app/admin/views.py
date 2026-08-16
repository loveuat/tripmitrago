from sqladmin import ModelView

from app.models.location import Location
from app.models.trip_type import TripType
from app.models.bookings import Booking
from app.models.contacts import Contact
from app.models.testimonials import Testimonial
from app.models.popular_routes import PopularRoute
from app.models.area_banner import AreaBanner

class LocationAdmin(ModelView, model=Location):
    list_template = "location_list.html"
    column_list = "__all__"
    column_searchable_list = [
        Location.name,
        Location.name_hi,
        Location.district,
        Location.sub_district,
        Location.pincode,
    ]


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

class ContactAdmin(ModelView, model=Contact):
    column_list = "__all__"

    column_searchable_list = [
        Contact.name,
        Contact.phone,
        Contact.email,
]

class TestimonialAdmin(ModelView, model=Testimonial):
    column_list = [
        Testimonial.id,
        Testimonial.name,
        Testimonial.designation,
        Testimonial.content,
        Testimonial.created_at,
    ]

class PopularRouteAdmin(
    ModelView,
    model=PopularRoute
):

    name = "Popular Route"
    name_plural = "Popular Routes"

    column_list = [
        PopularRoute.id,
        PopularRoute.image,
        PopularRoute.from_city,
        PopularRoute.to_city,
        PopularRoute.price,
        PopularRoute.distance,
        PopularRoute.trip_time,
        PopularRoute.created_at,
    ]

    column_searchable_list = [
        PopularRoute.from_city,
        PopularRoute.to_city,
    ]

class AreaBannerAdmin(ModelView, model=AreaBanner):
    name = "Area Banner"
    name_plural = "Area Banners (District/Tehsil)"
    column_list = [
        AreaBanner.id,
        AreaBanner.level,
        AreaBanner.name,
        AreaBanner.slug,
        AreaBanner.district_slug,
        AreaBanner.state,
        AreaBanner.banner_image,
    ]
    column_searchable_list = [AreaBanner.name, AreaBanner.slug]
    form_columns = [
        AreaBanner.level,
        AreaBanner.name,
        AreaBanner.slug,
        AreaBanner.district_slug,
        AreaBanner.state,
        AreaBanner.banner_image,
    ]