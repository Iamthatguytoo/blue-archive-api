from pydantic import BaseModel


class GachaPullSimulationResponse(BaseModel):
    simulations_conducted: int
    pulls_per_trial: int
    success_rate: float
    average_pulls_to_success: float
    median_pulls_to_success: float
    successful_runs: int
    zero_success: int
    trials_reached_spark: int
    max_pulls: int
    min_pulls: int
    natural_rate_up_obtained: int
    average_off_banner_3stars: float
    all_one_stars: int
    all_two_stars: int
    all_three_stars: int
    average_one_stars: float
    average_two_stars: float
    average_three_stars: float
    example_pull_log: list[str]
