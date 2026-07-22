from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.bookings import Booking

router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"]
)


@router.post("")
def create_booking(
    booking_data: dict,
    db: Session = Depends(get_db)
):
    booking = Booking(
        trip_type=booking_data.get("tripType"),

        pickup_location_id=booking_data.get("pickupLocationId"),
        pickup_location=booking_data.get("pickupLocation"),

        drop_location_id=booking_data.get("dropLocationId"),
        drop_location=booking_data.get("dropLocation"),

        pickup_date=booking_data.get("pickupDate"),
        pickup_time=booking_data.get("pickupTime"),

        passengers=booking_data.get("passengers"),
        car_type=booking_data.get("carType"),

        name=booking_data.get("name"),
        phone=booking_data.get("phone"),
        email=booking_data.get("email"),

        special_instructions=booking_data.get("specialInstructions"),

        status="pending"
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking created successfully",
        "booking_id": booking.id
    }