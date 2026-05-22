from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

def setup_ip_rate_limiting(server):
    server.state.limiter = limiter

    server.add_exception_handler(
        RateLimitExceeded,
        lambda request, exc: JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"}
        )
    )

    server.add_middleware(SlowAPIMiddleware)