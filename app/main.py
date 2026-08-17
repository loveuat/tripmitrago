import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from sqlalchemy import text
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine
from app.admin.auth import AdminAuth
from app.admin.views import (
    LocationAdmin,
    TripTypeAdmin,
    BookingAdmin,
    ContactAdmin,
    TestimonialAdmin,
    PopularRouteAdmin,
    AreaBannerAdmin
)

from app.routers.locations import router as locations_router
from app.routers.trip_types import router as trip_types_router
from app.routers.bookings import router as bookings_router
from app.routers.contacts import router as contacts_router
from app.routers.testimonials import router as testimonials_router
from app.routers.popular_routes import router as popular_routes_router
from app.routers.location_import import router as location_import_router
from app.routers.areas import router as areas_router
from app.routers.sitemap import router as sitemap_router

app = FastAPI(
    title="Trip Mitra GO",
    version="1.0.0"
)
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ridenova-chi.vercel.app",
        "https://www.tripmitrago.in"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Admin Authentication
authentication_backend = AdminAuth(
    secret_key=os.getenv("ADMIN_SECRET_KEY")
)


# SQLAdmin - CREATE ONLY ONCE
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    templates_dir="templates"
)


# Admin Menus
admin.add_view(LocationAdmin)
admin.add_view(TripTypeAdmin)
admin.add_view(BookingAdmin)
admin.add_view(ContactAdmin)
admin.add_view(TestimonialAdmin)
admin.add_view(PopularRouteAdmin)
admin.add_view(AreaBannerAdmin)

# API Routers
app.include_router(locations_router)
app.include_router(trip_types_router)
app.include_router(bookings_router)
app.include_router(contacts_router)
app.include_router(testimonials_router)
app.include_router(popular_routes_router)
app.include_router(location_import_router)
app.include_router(areas_router)
app.include_router(sitemap_router)
@app.get("/")
def root():
    return {
        "message": "Trip Mitra Go is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/database-health")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "error",
            "message": str(e)
        }
