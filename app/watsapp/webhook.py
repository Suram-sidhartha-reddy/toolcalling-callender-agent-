import os

from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


@router.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse(
        "Verification failed",
        status_code=403
    )


@router.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    print("\n========== WHATSAPP WEBHOOK ==========")
    print(data)
    print("======================================\n")

    return {"status": "received"}