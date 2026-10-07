from fastapi import APIRouter

from app.api.routes import chat, health


router = APIRouter()


router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

router.include_router(
    chat.router,
    prefix="/chat",
    tags=["Chat"],
)