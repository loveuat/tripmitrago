import os
import requests


def send_telegram_contact_notification(contact):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Telegram credentials missing")
        return False

    message = f"""
🚕 *NEW CONTACT ENQUIRY - Trip Mitra GO*

🆔 Contact ID: #{contact.id}

👤 *Customer Details*
Name: {contact.name}
📞 Phone: {contact.phone}
Subject: {contact.subject}
📧 Email: {contact.email}

📝 Message:
{contact.message or "None"}

🔴 Status: {contact.status}

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