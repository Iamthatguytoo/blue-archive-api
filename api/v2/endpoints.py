from fastapi import Depends, Request, Body, APIRouter
from schemas.v1.schema import (
    StudentFilter,
    CalcRequest,
    CalcResponse,
    PaginatedResponseModel,
    AnalyzePullsRequest,
    AnalyzePullsResponse,
)
from schemas.v2.schema import (
    GachaPullSparkSimulationRequest,
    GachaPullSparkSimulationResponse,
    GachaPullPitySimulationRequest,
    GachaPullPitySimulationResponse,
    )
from auth.v2.key_verification import verify_key
from auth.v2.create_random_key import generate_key
from middleware.v1.rate_limit import limiter
from services.v2.retrieve_students import fetch_students
from services.v1.gacha_calculate import calculate_gacha
from services.v2.gacha_simulate_spark import simulate_gacha_spark
from services.v2.gacha_simulate_pity import simulate_gacha_pity
from services.v1.analyze_pulls import pull_target
from services.v1.cache_requests import set_cache, get_cache
from docs_and_examples import doc_list
import logging

logger = logging.getLogger("blue-archive-api-v2")

blue_archive_api_v2_router = APIRouter()


##Create keys for clients endpoint
@blue_archive_api_v2_router.post(
    "/auth/register",
    tags=["keys"],
    summary=doc_list["keys"]["summary"],
    response_description=doc_list["keys"]["response_description"],
)
@limiter.limit("2/hour")
async def generate_api_key(request: Request):

    api_key_data = await generate_key()
    return {**api_key_data, "message": "Copy this string now. You wont see it again"}


##Get student data from DB endpoint
@blue_archive_api_v2_router.get(
    "/students",
    tags=["students"],
    summary=doc_list["students"]["summary"],
    response_description=doc_list["students"]["response_description"],
    response_model=PaginatedResponseModel,
)
@limiter.limit("60/minute")
async def get_students(
    request: Request,
    user=Depends(verify_key),
    name: str | None = None,
    base_name: str | None = None,
    limit: int = 20,
    skip: int = 0,
    filters: StudentFilter = Depends(),
):

    cache_key = f"v2:{name}:{base_name}:{limit}:{skip}:{filters}"

    cached = get_cache(cache_key)
    if cached:
        logger.info("CACHE HIT")
        return PaginatedResponseModel(**cached)

    logger.info("CACHE MISS")

    result = await fetch_students(
        filters=filters, name=name, base_name=base_name, limit=limit, skip=skip
    )

    set_cache(cache_key, result)

    return PaginatedResponseModel(**result)


##Calculate gacha pulls endpoint
@blue_archive_api_v2_router.post(
    "/gacha-calculate",
    tags=["gacha"],
    summary=doc_list["gacha-calculate"]["summary"],
    response_description=doc_list["gacha-calculate"]["response_description"],
    response_model=CalcResponse,
)
@limiter.limit("15/minute")
def calculate_odds(
    request: Request,
    pyroxene: CalcRequest = Body(example=doc_list["gacha-calculate"]["example"]),
    user=Depends(verify_key),
):

    result = calculate_gacha(pyroxene=pyroxene.pyroxene, rate_up=pyroxene.rate_up)
    return CalcResponse(**result)


##Simulate gacha(spark) endpoint
@blue_archive_api_v2_router.post(
    "/gacha-simulate/spark",
    tags=["gacha"],
    summary=doc_list["gacha-simulate-spark"]["summary"],
    response_description=doc_list["gacha-simulate-spark"]["response_description"],
    response_model=GachaPullSparkSimulationResponse,
)
@limiter.limit("15/minute")
def simulate_odds_spark(
    request: Request,
    all_pulls: GachaPullSparkSimulationRequest = Body(
        example=doc_list["gacha-simulate-spark"]["example"]
    ),
    user=Depends(verify_key),
):

    result = simulate_gacha_spark(
        simulations=all_pulls.simulations,
        pyroxene=all_pulls.pyroxene,
        featured_rate=all_pulls.featured_rate,
        three_star_rate=all_pulls.three_star_rate,
        continue_after_featured=all_pulls.continue_after_featured,
        pity_threshold=all_pulls.pity_threshold,
        spark_threshold=all_pulls.spark_threshold,
    )

    return GachaPullSparkSimulationResponse(**result)

##Simulate gacha(pity) endpoint
@blue_archive_api_v2_router.post(
    "/gacha-simulate/pity",
    tags=["gacha"],
    summary=doc_list["gacha-simulate-pity"]["summary"],
    response_description=doc_list["gacha-simulate-pity"]["response_description"],
    response_model=GachaPullPitySimulationResponse,
)
@limiter.limit("15/minute")
def simulate_odds_pity(
    request: Request,
    all_pulls: GachaPullPitySimulationRequest = Body(
        example=doc_list["gacha-simulate-pity"]["example"]
    ),
    user=Depends(verify_key),
):

    result = simulate_gacha_pity(
        simulations=all_pulls.simulations,
        pyroxene=all_pulls.pyroxene,
        featured_rate=all_pulls.featured_rate,
        continue_after_featured=all_pulls.continue_after_featured,
        three_star_rate=all_pulls.three_star_rate,
        pity_threshold=all_pulls.pity_threshold,
    )

    return GachaPullPitySimulationResponse(**result)

##Calculate pulls needed for a target probability endpoint
@blue_archive_api_v2_router.post(
    "/analyze-pulls",
    tags=["gacha"],
    summary=doc_list["analyze-pulls"]["summary"],
    response_description=doc_list["analyze-pulls"]["response_description"],
    response_model=AnalyzePullsResponse,
)
@limiter.limit("30/minute")
def target_pulls(
    request: Request,
    analyze_pulls: AnalyzePullsRequest = Body(
        example=doc_list["analyze-pulls"]["example"]
    ),
    user=Depends(verify_key),
):

    result = pull_target(
        probability=analyze_pulls.probability, rate_up=analyze_pulls.rate_up
    )

    return AnalyzePullsResponse(**result)
