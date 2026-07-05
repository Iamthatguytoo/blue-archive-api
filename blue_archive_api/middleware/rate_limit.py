from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


def get_real_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=get_real_ip)

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
