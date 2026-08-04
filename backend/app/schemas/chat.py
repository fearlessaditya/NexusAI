from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    filename: str
    uploaded_by: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]