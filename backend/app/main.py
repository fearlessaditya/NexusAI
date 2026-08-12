from fastapi import FastAPI
from app.core.config import settings
from app.api.user import router as user_router
from app.api.document import router as document_router
from app.api.chat import router as chat_router
from app.api.research import router as research_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(chat_router)
app.include_router(document_router)
app.include_router(research_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} 🚀",
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }