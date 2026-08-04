from fastapi import FastAPI
from app.core.config import settings
from app.api.user import router as user_router
from app.api.document import router as document_router
from app.api.chat import router as chat_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(user_router)
app.include_router(chat_router)
app.include_router(document_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} 🚀",
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }