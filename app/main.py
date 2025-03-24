from fastapi import FastAPI

from app.api import add_app_routes
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

add_app_routes(app)
