from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat.chat_service import ChatService
from app.api.dependencies import get_current_user,get_chat_service
from app.models import User

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post(
    "",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    response = chat_service.chat(
        question=request.question,
        owner_id=str(current_user.id),
        department=current_user.department,
        scope=request.scope
    )

    return ChatResponse(
        answer=response["answer"],
        sources=response["sources"]
    )