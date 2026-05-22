from fastapi import FastAPI, Depends, HTTPException, Request
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
        summary="Basic landing page when searching for this API",
        response_description="Greets you and checks if its running, shows you directions, and credits for creator of the API and the source for data"
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

##Create keys for clients endpoint
@server.post(
        "/auth/register",
        tags=["keys"],
        summary="Self serve endpoint to create keys",
        response_description="Prints out a key that contains 'sk_' and another 32 characters after that"
    )
@limiter.limit("2/hour")
def generate_api_key(request: Request):
    try:
        api_key_data = generate_key()
        return {
            **api_key_data,
            "message": "Copy this string now. You wont see it again"
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {e}")

##Get student data from DB endpoint
@server.get(
        "/students", 
        tags=["students"], 
        summary="Search for specific students with their stats in game", 
        response_description="Paginated list of students with their combat stats, equipment, affiliations, and terrain ratings", 
        response_model=PaginatedResponseModel
    )
@limiter.limit("60/minute")
def get_students(request: Request, user = Depends(verify_key) ,name: str = None, base_name: str = None, limit: int = 20, skip: int = 0, filters: StudentFilter = Depends()):
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
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

##Calculate gacha pulls endpoint
@server.post(
        "/gacha-calculate", 
        tags=["gacha"],
        summary="Calculate gacha pull probabilities and spark progress based on available pyroxene",
        response_description="Returns the total number of pulls, spark eligibility, remaining pulls needed to spark, probability of obtaining the rate-up naturally, and probability of requiring a spark",
        response_model=CalcResponse
    )
@limiter.limit("15/minute")
def calculate_odds(request: Request, pyroxene: CalcRequest, user = Depends(verify_key)):
    try:
        result = calculate_gacha(
            pyroxene=pyroxene.pyroxene,
            rate_up=pyroxene.rate_up
        )
        return CalcResponse(**result)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

##Simulate gacha endpoint
@server.post(
        "/gacha-simulate",
        tags=["gacha"],
        summary="Run Monte Carlo simulations to estimate gacha outcomes, spark frequency, and pull statistics",
        response_description="Returns simulation statistics including success rate, average and median pulls to success, spark occurrences, rate-up acquisition count, off-banner 3-star averages, and overall pull distribution metrics", 
        response_model=GachaPullSimulationResponse
    )
@limiter.limit("15/minute")
def simulate_odds(request: Request, all_pulls: GachaPullSimulationRequest, user = Depends(verify_key)):
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
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

##Calculate pulls needed for a target probability endpoint
@server.post(
        "/analyze-pulls",
        tags=["gacha"],
        summary="Calculate the pulls and pyroxene required to reach a target probability of obtaining the rate-up unit",
        response_description="Returns the estimated number of pulls, required pyroxene, target confidence level, and associated risk category for obtaining the rate-up unit",
        response_model=AnalyzePullsResponse
    )
@limiter.limit("30/minute")
def target_pulls(request: Request, analyze_pulls: AnalyzePullsRequest, user = Depends(verify_key)):
    try:
        result = pull_target(
            probability=analyze_pulls.probability,
            rate_up=analyze_pulls.rate_up
        )

        return AnalyzePullsResponse(**result)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error in server")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uv.run(server, host='0.0.0.0', port=port)