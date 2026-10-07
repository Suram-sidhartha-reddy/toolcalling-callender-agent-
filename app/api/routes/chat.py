from fastapi import APIRouter, Depends

from app.agent import run_agent
from app.dependencies.common import get_request_id
from app.schemas.chat import ChatRequest, ChatResponse


router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    request_id: str = Depends(get_request_id),
):
    response = run_agent(
        user_message=request.message,
        source=request.source,
        sender=request.sender,
    )

    return ChatResponse(
        response=response,
        request_id=request_id,
    )