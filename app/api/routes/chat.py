from fastapi import APIRouter, Depends

from app.dependencies.common import get_request_id
from app.dependencies.services import get_chat_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    request_id: str = Depends(get_request_id),
    service: ChatService = Depends(get_chat_service),
):
    return service.process_chat(
        request=request,
        request_id=request_id,
    )