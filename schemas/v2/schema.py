from pydantic import BaseModel, Field, model_validator

class GachaPullPitySimulationRequest(BaseModel):
    simulations: int = Field(..., gt=0, le=1000)
    pyroxene: int = Field(..., ge=120)
    featured_rate: float = Field(0.007, gt=0, lt=1)
    continue_after_featured: bool = Field(True)
    three_star_rate: float = Field(0.03, gt=0, lt=1)
    pity_threshold: int = Field(100, gt=0)

    @model_validator(mode="after")
    def validate_fields(self):

        if self.featured_rate > self.three_star_rate:
            raise ValueError("featured_rate cannot be greater than three_star_rate")

        return self

class GachaPullSparkSimulationRequest(BaseModel):
    simulations: int = Field(..., gt=0, le=1000)
    pyroxene: int = Field(..., ge=120)
    featured_rate: float = Field(0.007, gt=0, lt=1)
    three_star_rate: float = Field(0.03, gt=0, lt=1)
    continue_after_featured: bool = Field(True)
    pity_threshold: int = Field(100, gt=0)
    spark_threshold: int = Field(200, gt=0)

    @model_validator(mode="after")
    def validate_fields(self):
        if self.pity_threshold >= self.spark_threshold:
            raise ValueError("pity_threshold must be less than spark_threshold")

        if self.featured_rate > self.three_star_rate:
            raise ValueError("featured_rate cannot be greater than three_star_rate")

        return self
    
class GachaPullPitySimulationResponse(BaseModel):
    simulations_conducted: int
    pulls_per_trial: int
    success_rate: float
    average_pulls_to_success: float
    median_pulls_to_success: float
    successful_runs: int
    zero_success: int
    max_pulls: int
    min_pulls: int
    natural_featured_trials_count: int
    average_off_banner_3stars: float
    all_one_stars: int
    all_two_stars: int
    all_three_stars: int
    average_one_stars: float
    average_two_stars: float
    average_three_stars: float
    example_pull_log: list[str]

class GachaPullSparkSimulationResponse(BaseModel):
    simulations_conducted: int
    pulls_per_trial: int
    success_rate: float
    average_pulls_to_success: float
    median_pulls_to_success: float
    successful_runs: int
    zero_success: int
    trials_reached_spark: int
    spark_rate: float
    max_pulls: int
    min_pulls: int
    natural_featured_trials_count: int
    sparked_featured_trials_count: int
    total_featured_obtained: int
    average_off_banner_3stars: float
    all_one_stars: int
    all_two_stars: int
    all_three_stars: int
    average_one_stars: float
    average_two_stars: float
    average_three_stars: float
    example_pull_log: list[str]
