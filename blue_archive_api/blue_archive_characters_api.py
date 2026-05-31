from fastapi import FastAPI, Depends, HTTPException, Request, Body
import uvicorn as uv
from models import StudentFilter, CalcRequest, CalcResponse, GachaPullSimulationRequest, GachaPullSimulationResponse, PaginatedResponseModel, AnalyzePullsRequest, AnalyzePullsResponse
from auth.create_random_key import generate_key
from auth.key_verification import verify_key
from middleware.rate_limit import limiter, setup_ip_rate_limiting
from services.retrieve_students import fetch_students
from services.gacha_calculate import calculate_gacha
from services.gacha_simulate import simulate_gacha
from services.analyze_pulls import pull_target
from services.cache_requests import set_cache, get_cache
from docs_and_examples import doc_list
import logging
import os
import time

server = FastAPI(title="Fan-Made Blue Archive API", version="1.0.0")

setup_ip_rate_limiting(server=server)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("blue-archive-api")

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
    try: 
        return {
            "message": "Hello! Welcome to the Blue Archive API",
            "status": "running",
            "docs": "/docs",
            "redoc": "/redoc",
            "created_by(github)": "Iamthatguytoo",
            "credits": "Character data sourced from Blue Archive Wiki. Retrieved from Blue Archive Wiki Characters page. A big thanks to the Blue Archive Wiki team for their hard work." 
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

## Health check endpoint
@server.get("/health")
def health_check():
    try:
         return {"status": "healthy"}
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=503, detail="Services are unavailable. Please try again later")


##Create keys for clients endpoint
@server.post(
        "/auth/register",
        tags=["keys"],
        summary=doc_list["keys"]["summary"],
        response_description=doc_list["keys"]["response_description"]
    )
@limiter.limit("2/hour")
def generate_api_key(request: Request):
    try:
        api_key_data = generate_key()
        return {
            **api_key_data,
            "message": "Copy this string now. You wont see it again"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")

##Get student data from DB endpoint
@server.get(
        "/students", 
        tags=["students"], 
        summary=doc_list["students"]["summary"], 
        response_description=doc_list["students"]["response_description"], 
        response_model=PaginatedResponseModel
    )
@limiter.limit("60/minute")
def get_students(request: Request, user = Depends(verify_key) ,name: str | None = None, base_name: str | None = None, limit: int = 20, skip: int = 0, filters: StudentFilter = Depends()):
    try:
        cache_key = f"{name}:{base_name}:{limit}:{skip}:{filters}"

        cached = get_cache(cache_key)
        if cached:
           logger.info("CACHE HIT")
           return PaginatedResponseModel(**cached)
        
        logger.info("CACHE MISS")

        result = fetch_students(
            filters=filters,
            name=name,
            base_name=base_name,
            limit=limit,
            skip=skip
        )

        set_cache(cache_key, result)

        return PaginatedResponseModel(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

##Calculate gacha pulls endpoint
@server.post(
        "/gacha-calculate", 
        tags=["gacha"],
        summary=doc_list["gacha-calculate"]["summary"],
        response_description=doc_list["gacha-calculate"]["response_description"],
        response_model=CalcResponse
    )
@limiter.limit("15/minute")
def calculate_odds(request: Request, pyroxene: CalcRequest = Body(example=doc_list["gacha-calculate"]["example"]), user = Depends(verify_key)):
    try:
        result = calculate_gacha(
            pyroxene=pyroxene.pyroxene,
            rate_up=pyroxene.rate_up
        )
        return CalcResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

##Simulate gacha endpoint
@server.post(
        "/gacha-simulate",
        tags=["gacha"],
        summary=doc_list["gacha-simulate"]["summary"],
        response_description=doc_list["gacha-simulate"]["response_description"], 
        response_model=GachaPullSimulationResponse
    )
@limiter.limit("15/minute")
def simulate_odds(request: Request, all_pulls: GachaPullSimulationRequest = Body(example=doc_list["gacha-simulate"]["example"]), user = Depends(verify_key)):
    if all_pulls.simulations > 1000:
        raise HTTPException(status_code=400, detail="Simulations cannot exceed 1000")
    try:
        result = simulate_gacha(
            simulations=all_pulls.simulations,
            pyroxene=all_pulls.pyroxene,
            rate_up=all_pulls.rate_up,
            rate_up_3_star=all_pulls.rate_up_3_star,
            pity_threshold=all_pulls.pity_threshold,
            spark_threshold=all_pulls.spark_threshold
        )

        return GachaPullSimulationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

##Calculate pulls needed for a target probability endpoint
@server.post(
        "/analyze-pulls",
        tags=["gacha"],
        summary=doc_list["analyze-pulls"]["summary"],
        response_description=doc_list["analyze-pulls"]["response_description"], 
        response_model=AnalyzePullsResponse
    )
@limiter.limit("30/minute")
def target_pulls(request: Request, analyze_pulls: AnalyzePullsRequest = Body(example=doc_list["analyze-pulls"]["example"]), user = Depends(verify_key)):
    try:
        result = pull_target(
            probability=analyze_pulls.probability,
            rate_up=analyze_pulls.rate_up
        )

        return AnalyzePullsResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uv.run(server, host='0.0.0.0', port=port)
