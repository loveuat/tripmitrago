import os
import httpx


async def verify_turnstile(token: str) -> bool:
    secret = os.getenv("TURNSTILE_SECRET_KEY")

    if not secret or not token:
        return False

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": secret,
                "response": token,
            },
        )

    result = response.json()

    return result.get("success", False)