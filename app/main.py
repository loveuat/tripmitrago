import os

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from sqlalchemy import text
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.admin.auth import AdminAuth
from app.admin.views import (
    LocationAdmin,
    TripTypeAdmin,
    BookingAdmin,
)

from app.routers.locations import router as locations_router
from app.routers.trip_types import router as trip_types_router
from app.routers.bookings import router as bookings_router


app = FastAPI(
    title="Trip Mitra GO",
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ridenova-chi.vercel.app/",
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
    authentication_backend=authentication_backend
)


# Admin Menus
admin.add_view(LocationAdmin)
admin.add_view(TripTypeAdmin)
admin.add_view(BookingAdmin)


# API Routers
app.include_router(locations_router)
app.include_router(trip_types_router)
app.include_router(bookings_router)


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