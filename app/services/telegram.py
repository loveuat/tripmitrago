import os
import requests


def send_telegram_notification(booking):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Telegram credentials missing")
        return False

    message = f"""
🚕 *NEW BOOKING - Trip Mitra GO*

🆔 Booking ID: #{booking.id}

📍 *Pickup*
{booking.pickup_location}

📍 *Drop*
{booking.drop_location}

📅 Date: {booking.pickup_date}
⏰ Time: {booking.pickup_time}

🚗 Trip Type: {booking.trip_type}
🚙 Car Type: {booking.car_type}
👥 Passengers: {booking.passengers}

👤 *Customer Details*
Name: {booking.name}
📞 Phone: {booking.phone}
📧 Email: {booking.email}

📝 Instructions:
{booking.special_instructions or "None"}

🔴 Status: {booking.status}

👉 Please contact the customer.
""".strip()

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        print("Telegram notification sent successfully")

        return True

    except requests.RequestException as e:
        print("Telegram notification failed:", e)

        return False