from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import ask_question

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/ask",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    response = ask_question(request.question)

    return response