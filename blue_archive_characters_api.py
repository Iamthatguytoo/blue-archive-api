from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
import uvicorn as uv
from middleware.rate_limit import setup_ip_rate_limiting
from docs_and_examples import tags_metadata
from api.v1.endpoints import blue_archive_api_v1_router
from docs_and_examples import doc_list
from services.health_check import create_health_check
import logging
import os
import time

server = FastAPI(
    title="Fan-Made Blue Archive API",
    description="A fan-made REST API for Blue Archive data.",
    contact={
        "name": "Iamthatguytoo",
        "url": "https://github.com/Iamthatguytoo",
    },
    version="1.0.0",
    openapi_tags=tags_metadata
    )

setup_ip_rate_limiting(server=server)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("blue-archive-api")

## Global Exception Handler
@server.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error")

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error"
        },
    )

# Global ValidationError Handler
@server.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "status": "error",
            "message": "Invalid input",
            "details": exc.errors(),
        }),
    )

##Log each action middleware
@server.middleware("http")
async def log_request(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    logger.info(
        f"{request.method} {request.url.path} | "
        f"status={response.status_code} | "
        f"time={duration:.3f}s"
        )
    
    return response

##Basic welcome page endpoint
@server.get(
    "/",
    summary=doc_list["/"]["summary"],
    response_description=doc_list["/"]["response_description"]
)
def show_api_working():
    return {
        "message": "Hello! Welcome to the Blue Archive API",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": "1.0.0",
        "created_by(github)": "Iamthatguytoo",
        "credits": "Character data sourced from Blue Archive Wiki. Retrieved from Blue Archive Wiki Characters page. A big thanks to the Blue Archive Wiki team for their hard work." 
    }

## Health check endpoint
@server.get(
    "/health",
    summary=doc_list["health"]["summary"],
    response_description=doc_list["health"]["response_description"]
)
def health_check():
    return create_health_check()

##Import the Router(versioned)
server.include_router(
    blue_archive_api_v1_router,
    prefix="/v1"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uv.run(server, host='0.0.0.0', port=port)