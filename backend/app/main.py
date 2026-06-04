from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title="DocuAware API",
    version="1.0.0"
)

app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} API Running",
        "environment":settings.environment
    }