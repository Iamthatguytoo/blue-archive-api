from pydantic import BaseModel, Field
from typing import Optional, Literal

class Terrain(BaseModel):
    urban_terrain: Optional[str]
    outdoor_terrain: Optional[str]
    indoor_terrain: Optional[str]

class StudentResponse(BaseModel):
    name: str
    base_name: str
    rarity: Optional[str]
    variant: Optional[str]

    damage_type: Optional[str]
    armor_type: Optional[str]
    class_name: Optional[str]

    school: Optional[str]
    position: Optional[str]
    weapon: Optional[str]
    pool: Optional[str]

    terrain: Terrain

class PaginatedResponseModel(BaseModel):
    total: int
    skip: int
    limit: int
    students: list[StudentResponse]

class CalcRequest(BaseModel):
    pyroxene: int = Field(..., ge=0)
    rate_up: float = Field(0.007, gt=0, lt=1)

class CalcResponse(BaseModel):
    pulls: int
    spark_reachable: bool
    pulls_to_spark: int
    chance_get_rate_up_naturally: float
    chance_need_spark: float
    
class GachaPullSimulationRequest(BaseModel):
    simulations: int = Field(..., gt=0, le=10000)
    pyroxene: int = Field(..., ge=0)
    rate_up: float = Field(0.007, gt=0, lt=1)
    rate_up_3_star: float = Field(0.03, gt=0, lt=1)
    pity_threshold: int = Field(100, gt=0)
    spark_threshold: int = Field(200, gt=0)

class GachaPullSimulationResponse(BaseModel):
    simulations_conducted: int
    pulls_per_trial: int
    success_rate: float
    average_pulls_to_success: float
    median_pulls_to_success: float
    succesful_runs: int
    zero_success: int
    trials_reached_spark: int
    max_pulls: int
    min_pulls: int
    rate_up_obtained: int
    average_off_banner_3stars: float

class AnalyzePullsRequest(BaseModel):
    probability: float = Field(..., ge=0, le=1)
    rate_up: float = Field(0.007, gt=0, le=1)

class AnalyzePullsResponse(BaseModel):
    required_pulls: int
    pyroxene_needed: int
    confidence: float
    risk_level: Literal["low", "moderate", "high"]

class StudentFilter(BaseModel):
    school: Optional[str] = None
    position: Optional[str] = None
    damage_type: Optional[str] = None
