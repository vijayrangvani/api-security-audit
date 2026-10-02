import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        client_ip = request.client.host
        current_time = time.time()

        requests = self.clients.get(client_ip, [])

        requests = [
            timestamp
            for timestamp in requests
            if current_time - timestamp < self.window_seconds
        ]

        if len(requests) >= self.max_requests:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"}
            )

        requests.append(current_time)
        self.clients[client_ip] = requests

        return await call_next(request)