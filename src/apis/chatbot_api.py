from fastapi import APIRouter, Depends
from ..schemas.chatbot_schema import ChatRequest, ChatResponse
from ..services.chatbot_service import get_chatbot_service, ChatbotService

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, service: ChatbotService = Depends(get_chatbot_service)):
    response = service.chat(request.message, request.history)
    return ChatResponse(message=response)
