from __future__ import annotations

import json
import logging
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        event: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        http_context = getattr(record, "http", None)
        if http_context is not None:
            event["http"] = http_context
        return json.dumps(event, default=str)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["x-correlation-id"] = correlation_id
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        logging.getLogger("atlas.http").info(
            "request_complete",
            extra={
                "http": {
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "duration_ms": elapsed_ms,
                    "correlation_id": correlation_id,
                    "headers": dict(request.headers),
                }
            },
        )
        return response
