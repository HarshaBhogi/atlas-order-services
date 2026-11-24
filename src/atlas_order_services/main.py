from __future__ import annotations

from fastapi import FastAPI

from .config import get_settings
from .errors import install_error_handlers
from .observability import RequestContextMiddleware, configure_logging
from .routers import probes, router


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(RequestContextMiddleware)
    app.include_router(probes)
    app.include_router(router)
    install_error_handlers(app)
    return app


app = create_app()
