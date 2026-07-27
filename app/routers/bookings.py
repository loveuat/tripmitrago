from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.bookings import Booking
from app.services.telegram import send_telegram_notification


router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"]
)


@router.post("")
def create_booking(
    booking_data: dict,
    db: Session = Depends(get_db)
):

    try:

        print("========== BOOKING REQUEST START ==========")

        # Debug incoming data
        print("1. Booking Data:")
        print(booking_data)


        # Create Booking
        print("2. Creating Booking object...")

        booking = Booking(
            trip_type=booking_data.get("tripType"),

            pickup_location_id=booking_data.get(
                "pickupLocationId"
            ),
            pickup_location=booking_data.get(
                "pickupLocation"
            ),

            drop_location_id=booking_data.get(
                "dropLocationId"
            ),
            drop_location=booking_data.get(
                "dropLocation"
            ),

            pickup_date=booking_data.get(
                "pickupDate"
            ),
            pickup_time=booking_data.get(
                "pickupTime"
            ),

            passengers=booking_data.get(
                "passengers"
            ),
            car_type=booking_data.get(
                "carType"
            ),

            name=booking_data.get(
                "name"
            ),
            phone=booking_data.get(
                "phone"
            ),
            email=booking_data.get(
                "email"
            ),

            special_instructions=booking_data.get(
                "specialInstructions"
            ),

            status="pending"
        )


        # Save Booking
        print("3. Adding booking to database...")

        db.add(booking)

        print("4. Committing database...")

        db.commit()

        print(
            "5. Database commit successful"
        )


        # Refresh Booking
        db.refresh(booking)

        print(
            "6. Booking ID:",
            booking.id
        )


        # Telegram Notification
        try:

            print(
                "7. Sending Telegram notification..."
            )

            send_telegram_notification(
                booking
            )

            print(
                "8. Telegram notification sent successfully"
            )

        except Exception as telegram_error:

            print(
                "❌ Telegram ERROR:",
                repr(telegram_error)
            )


        # Response
        response = {
            "message": "Booking created successfully",
            "success": True,
            "booking_id": booking.id
        }

        print(
            "9. Final Response:",
            response
        )

        print(
            "========== BOOKING REQUEST END =========="
        )

        return response


    except Exception as e:

        print(
            "🔥 BOOKING API ERROR:",
            repr(e)
        )

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )