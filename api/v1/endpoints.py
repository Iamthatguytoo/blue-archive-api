from fastapi import Depends, Request, Body, APIRouter
from models import StudentFilter, CalcRequest, CalcResponse, GachaPullSimulationRequest, GachaPullSimulationResponse, PaginatedResponseModel, AnalyzePullsRequest, AnalyzePullsResponse
from auth.key_verification import verify_key
from auth.create_random_key import generate_key
from middleware.rate_limit import limiter
from services.retrieve_students import fetch_students
from services.gacha_calculate import calculate_gacha
from services.gacha_simulate import simulate_gacha
from services.health_check import create_health_check
from services.analyze_pulls import pull_target
from services.cache_requests import set_cache, get_cache
from docs_and_examples import doc_list
import logging

logger = logging.getLogger("blue-archive-api-v1")

blue_archive_api_v1_router = APIRouter()

##Basic welcome page endpoint
@blue_archive_api_v1_router.get(
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
@blue_archive_api_v1_router.get(
    "/health",
    summary=doc_list["health"]["summary"],
    response_description=doc_list["health"]["response_description"]
)
def health_check():
    return create_health_check()

##Create keys for clients endpoint
@blue_archive_api_v1_router.post(
    "/auth/register",
    tags=["keys"],
    summary=doc_list["keys"]["summary"],
    response_description=doc_list["keys"]["response_description"]
)
@limiter.limit("2/hour")
def generate_api_key(request: Request):
    
    api_key_data = generate_key()
    return {
        **api_key_data,
        "message": "Copy this string now. You wont see it again"
    }

##Get student data from DB endpoint
@blue_archive_api_v1_router.get(
        "/students", 
        tags=["students"], 
        summary=doc_list["students"]["summary"], 
        response_description=doc_list["students"]["response_description"], 
        response_model=PaginatedResponseModel
    )
@limiter.limit("60/minute")
def get_students(request: Request, user = Depends(verify_key), name: str | None = None, base_name: str | None = None, limit: int = 20, skip: int = 0, filters: StudentFilter = Depends()):
    
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

##Calculate gacha pulls endpoint
@blue_archive_api_v1_router.post(
    "/gacha-calculate", 
    tags=["gacha"],
    summary=doc_list["gacha-calculate"]["summary"],
    response_description=doc_list["gacha-calculate"]["response_description"],
    response_model=CalcResponse
)
@limiter.limit("15/minute")
def calculate_odds(request: Request, pyroxene: CalcRequest = Body(example=doc_list["gacha-calculate"]["example"]), user = Depends(verify_key)):
    
    result = calculate_gacha(
        pyroxene=pyroxene.pyroxene,
        rate_up=pyroxene.rate_up
    )
    return CalcResponse(**result)

##Simulate gacha endpoint
@blue_archive_api_v1_router.post(
    "/gacha-simulate",
    tags=["gacha"],
    summary=doc_list["gacha-simulate"]["summary"],
    response_description=doc_list["gacha-simulate"]["response_description"], 
    response_model=GachaPullSimulationResponse
)
@limiter.limit("15/minute")
def simulate_odds(request: Request, all_pulls: GachaPullSimulationRequest = Body(example=doc_list["gacha-simulate"]["example"]), user = Depends(verify_key)):
        
    result = simulate_gacha(
        simulations=all_pulls.simulations,
        pyroxene=all_pulls.pyroxene,
        rate_up=all_pulls.rate_up,
        rate_up_3_star=all_pulls.rate_up_3_star,
        pity_threshold=all_pulls.pity_threshold,
        spark_threshold=all_pulls.spark_threshold
    )

    return GachaPullSimulationResponse(**result)

##Calculate pulls needed for a target probability endpoint
@blue_archive_api_v1_router.post(
    "/analyze-pulls",
    tags=["gacha"],
    summary=doc_list["analyze-pulls"]["summary"],
    response_description=doc_list["analyze-pulls"]["response_description"], 
    response_model=AnalyzePullsResponse
)

@limiter.limit("30/minute")
def target_pulls(request: Request, analyze_pulls: AnalyzePullsRequest = Body(example=doc_list["analyze-pulls"]["example"]), user = Depends(verify_key)):
        
    result = pull_target(
        probability=analyze_pulls.probability,
        rate_up=analyze_pulls.rate_up
    )

    return AnalyzePullsResponse(**result)