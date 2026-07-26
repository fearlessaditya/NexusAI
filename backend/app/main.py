from fastapi import FastAPI
from app.core.config import settings
from app.api.user import router as user_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} 🚀",
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }