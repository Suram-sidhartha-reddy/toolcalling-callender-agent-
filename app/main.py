from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import router
from app.middleware.request_id import RequestIDMiddleware

from app.domain.exceptions import ConversationNotFoundError


app = FastAPI(
    title="Calendar AI Agent",
    description="AI-powered Google Calendar agent",
    version="1.0.0",
)


# ----------------------------------------
# Middleware
# ----------------------------------------

app.add_middleware(RequestIDMiddleware)


# ----------------------------------------
# API routes
# ----------------------------------------

app.include_router(
    router,
    prefix="/api/v1",
)


# ----------------------------------------
# Global exception handler
# ----------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred.",
            "request_id": getattr(
                request.state,
                "request_id",
                None,
            ),
        },
    )

@app.exception_handler(ConversationNotFoundError)
async def conversation_not_found_handler(
    request: Request,
    exc: ConversationNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "conversation_not_found",
            "message": str(exc),
            "request_id": getattr(
                request.state,
                "request_id",
                None,
            ),
        },
    )