import random
import statistics
from fastapi import HTTPException

def simulate_gacha(
        simulations: int, 
        pyroxene: int,
        rate_up: float,
        rate_up_3_star: float,
        pity_threshold: int,
        spark_threshold: int
        ):
    if simulations > 1000:
        raise HTTPException(status_code=400, detail="Simulations cannot exceed 1000")
    total_pulls = []
    total_rate_up_natural = []
    total_off_banner_3_stars = []
    spark_count = 0
    total_successes = []
            
    pulls_per_trial = pyroxene // 120
    if pulls_per_trial == 0:
        raise HTTPException(status_code=400, detail='Not enough Pyroxenes for pulling')         

    for _ in range(simulations):
        pulls = pulls_per_trial
        success = False
        pull_count = 0
        pity_count = 0
        rate_up_natural = False
        off_banner_3_stars = 0
                
        for _ in range(pulls):
            pull_count += 1
            pity_count += 1

            if pull_count >= spark_threshold:
                success = True
                spark_count += 1
                break
                    
            is_3_star = pity_count >= pity_threshold or random.random() < rate_up_3_star

            if is_3_star:
                pity_count = 0
                is_rate_up_unit =  random.random() < (rate_up / rate_up_3_star)
                if is_rate_up_unit:
                    success = True
                    rate_up_natural = True
                    break
                else:
                    off_banner_3_stars += 1

        total_pulls.append(pull_count)
        total_successes.append(success)
        total_rate_up_natural.append(rate_up_natural)
        total_off_banner_3_stars.append(off_banner_3_stars)
                
    max_pulls = max(total_pulls)
    min_pulls = min(total_pulls)

    success_trials = sum(total_successes) / simulations
    succesful_runs = total_successes.count(True)
    zero_success = total_successes.count(False)
    average_pulls_to_success = (sum(total_pulls) / simulations if simulations > 0 else 0)
    median_pulls_to_success = statistics.median(total_pulls)
    rate_up_natural_count = total_rate_up_natural.count(True)
    average_off_banner_3stars = round(sum(total_off_banner_3_stars) / simulations, 2)

    return {
        "simulations_conducted": simulations,
        "pulls_per_trial": pulls_per_trial,
        "success_rate": success_trials,
        "average_pulls_to_success": round(average_pulls_to_success, 2),
        "median_pulls_to_success": round(median_pulls_to_success, 2),
        "succesful_runs": succesful_runs,
        "zero_success": zero_success,
        "trials_reached_spark": spark_count,
        "max_pulls": max_pulls,
        "min_pulls": min_pulls,
        "rate_up_obtained": rate_up_natural_count,
        "average_off_banner_3stars": average_off_banner_3stars
    }