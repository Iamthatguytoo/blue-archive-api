from utils.gacha_pulls import pull_spark
import statistics


def simulate_gacha(
    simulations: int,
    pyroxene: int,
    rate_up: float,
    rate_up_3_star: float,
    pity_threshold: int,
    spark_threshold: int,
):
    total_pulls = []
    total_rate_up_natural = []
    total_off_banner_3_stars = []
    spark_count = 0
    total_successes = []

    pulls_per_trial = pyroxene // 120

    for _ in range(simulations):
        pulls = pulls_per_trial
        success = False
        pull_count = 0
        three_star_pity_count = 0
        rate_up_natural = False
        off_banner_3_stars = 0

        for start in range(0, pulls, 10):
            pulls_in_batch = min(10, pulls - start)

            for _ in range(pulls_in_batch):
                pull_count += 1
                three_star_pity_count += 1

                result = pull_spark(
                    three_star_pity_count=three_star_pity_count,
                    pull_count=pull_count,
                    spark_threshold=spark_threshold,
                    pity_threshold=pity_threshold,
                    featured_rate=rate_up,
                    three_star_rate=rate_up_3_star,
                )

                three_star_pity_count = result["three_star_pity_count"]
                off_banner_3_stars += result["off_banner"]

                if result["spark"]:
                    spark_count += 1

                if result["success"]:
                    success = True
                    rate_up_natural = result["natural_featured"]
                    break

            if success:
                break

        total_pulls.append(pull_count)
        total_successes.append(success)
        total_rate_up_natural.append(rate_up_natural)
        total_off_banner_3_stars.append(off_banner_3_stars)

    max_pulls = max(total_pulls)
    min_pulls = min(total_pulls)

    success_trials = sum(total_successes) / simulations
    successful_runs = total_successes.count(True)
    zero_success = total_successes.count(False)
    successful_pull_counts = [
        pulls for pulls, success in zip(total_pulls, total_successes) if success
    ]
    average_pulls_to_success = (
        sum(successful_pull_counts) / len(successful_pull_counts)
        if successful_pull_counts
        else None
    )
    median_pulls_to_success = (
        statistics.median(successful_pull_counts) if successful_pull_counts else None
    )
    rate_up_natural_count = total_rate_up_natural.count(True)
    average_off_banner_3stars = round(sum(total_off_banner_3_stars) / simulations, 2)

    return {
        "simulations_conducted": simulations,
        "pulls_per_trial": pulls_per_trial,
        "success_rate": success_trials,
        "average_pulls_to_success": (
            round(average_pulls_to_success, 2)
            if average_pulls_to_success is not None
            else None
        ),
        "median_pulls_to_success": (
            round(median_pulls_to_success, 2)
            if median_pulls_to_success is not None
            else None
        ),
        "successful_runs": successful_runs,
        "zero_success": zero_success,
        "trials_reached_spark": spark_count,
        "max_pulls": max_pulls,
        "min_pulls": min_pulls,
        "natural_rate_up_obtained": rate_up_natural_count,
        "average_off_banner_3stars": average_off_banner_3stars,
    }
