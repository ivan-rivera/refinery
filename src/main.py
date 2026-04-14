"""FastAPI application entry point."""

from fastapi import FastAPI

from src.api.routes import router
from src.config.logging import configure_logging
from src.config.settings import get_settings

settings = get_settings()
configure_logging(settings.app_log_level)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)
app.include_router(router, prefix="/api")
