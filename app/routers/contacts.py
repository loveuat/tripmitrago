import os
import requests

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.turnstile import verify_turnstile
from app.database import get_db
from app.models.contacts import Contact
from app.schemas.contacts import ContactCreate
from app.services.telegram_contact import send_telegram_contact_notification


router = APIRouter(
    prefix="/api/v1/contacts",
    tags=["Contacts"]
)


@router.post("")
async def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db)
):

    try:

        print("========== CONTACT REQUEST START ==========")

        # Debug: Incoming data
        print(
            "1. Contact Data:",
            contact_data.model_dump()
        )


        # Verify Cloudflare Turnstile
        print("2. Verifying Turnstile...")

        is_valid = await verify_turnstile(
            contact_data.turnstile_token
        )

        print(
            "3. Turnstile Result:",
            is_valid
        )

        if not is_valid:
            print(
                "4. Turnstile Verification FAILED"
            )

            raise HTTPException(
                status_code=400,
                detail="Turnstile verification failed"
            )


        # Create Contact
        print("5. Creating Contact object...")

        contact = Contact(
            **contact_data.model_dump(
                exclude={"turnstile_token"}
            ),
            status="new"
        )

        print(
            "6. Contact Object:",
            contact
        )


        # Save Contact
        print("7. Adding contact to database...")

        db.add(contact)

        print("8. Committing database...")

        db.commit()

        print(
            "9. Database commit successful"
        )


        # Refresh Contact
        db.refresh(contact)

        print(
            "10. Contact ID:",
            contact.id
        )


        # Telegram Notification
        print(
            "11. Sending Telegram notification..."
        )

        send_telegram_contact_notification(contact)

        print(
            "12. Telegram notification sent"
        )


        # Final Response
        response = {
            "message": "Thank you for contacting us.",
            "success": True,
            "id": contact.id
        }

        print(
            "13. Final Response:",
            response
        )

        print(
            "========== CONTACT REQUEST END =========="
        )

        return response


    except HTTPException:
        raise


    except Exception as e:

        print(
            "🔥 CONTACT API ERROR:",
            repr(e)
        )

        print(
            "🔥 ERROR TYPE:",
            type(e).__name__
        )

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )