
from app.config import settings


def send_sms(phone: str, message: str) -> dict:

    if settings.PROVIDER_MODE == "mock":

        print("--------------------------------")
        print("MOCK SMS SERVICE")
        print("--------------------------------")

        print(f"Phone: {phone}")
        print(f"Message: {message}")

        return {
            "status": "simulated",
            "provider_message_id": None
        }

    raise RuntimeError(
        "Production SMS provider is not configured"
    )
