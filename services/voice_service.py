
from app.config import settings


def make_call(phone: str) -> dict:

    if settings.PROVIDER_MODE == "mock":

        print("--------------------------------")
        print("MOCK VOICE CALL SERVICE")
        print("--------------------------------")

        print(f"Calling Number: {phone}")

        return {
            "status": "simulated",
            "provider_message_id": None
        }

    raise RuntimeError(
        "Production voice provider is not configured"
    )
