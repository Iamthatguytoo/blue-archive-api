from utils.gacha_pulls import pull_spark
import statistics


def simulate_gacha_spark(
    simulations: int,
    pyroxene: int,
    featured_rate: float,
    three_star_rate: float,
    continue_after_featured: bool,
    pity_threshold: int,
    spark_threshold: int,
):
    total_pulls = []
    total_natural_featured = []
    total_off_banner_3_stars = []
    spark_count = 0
    total_sparked_featured = []
    total_featured_pull_counts = []
    total_successes = []
    total_one_stars = []
    total_two_stars = []
    total_three_stars = []
    example_pull_log = None

    pulls_per_trial = pyroxene // 120

    for sim in range(simulations):
        pulls = pulls_per_trial
        success = False
        pull_count = 0
        three_star_pity_count = 0
        natural_featured = False
        sparked_featured = False
        reached_spark = False
        featured_pull = None
        off_banner_3_stars = 0
        pull_log = []
        one_stars = 0
        two_stars = 0
        three_stars = 0

        
        for start in range(0, pulls, 10):
            batch_log = []
            pulls_in_batch = min(10, pulls - start)

            for _ in range(pulls_in_batch):
                pull_count += 1
                three_star_pity_count += 1

                result = pull_spark(
                    three_star_pity_count=three_star_pity_count,
                    pull_count=pull_count,
                    spark_threshold=spark_threshold,
                    pity_threshold=pity_threshold,
                    featured_rate=featured_rate,
                    three_star_rate=three_star_rate,
                )

                three_star_pity_count = result["three_star_pity_count"]
                off_banner_3_stars += result["off_banner"]

                if result["rarity"] == 3:
                    three_stars += 1
                elif result["rarity"] == 2:
                    two_stars += 1
                elif result["rarity"] == 1:
                    one_stars += 1

                if result["spark"]:
                    reached_spark = True

                if result["featured"]:
                    if not success:
                        success = True
                        featured_pull = pull_count

                        if result["natural_featured"]:
                            natural_featured = True
                        elif result["spark"]:
                            sparked_featured = True

                    if not continue_after_featured:
                        break

                batch_log.append(f"{result['rarity']}★")

            pull_log.append(batch_log)

            if not continue_after_featured and success:
                break

        if sim == 0:
            example_pull_log = pull_log[0]

        if reached_spark:
            spark_count += 1

        if featured_pull is not None:
                total_featured_pull_counts.append(featured_pull)

        total_pulls.append(pull_count)
        total_successes.append(success)
        total_natural_featured.append(natural_featured)
        total_sparked_featured.append(sparked_featured)
        total_off_banner_3_stars.append(off_banner_3_stars)
        total_one_stars.append(one_stars)
        total_two_stars.append(two_stars)
        total_three_stars.append(three_stars)

    max_pulls = max(total_featured_pull_counts)
    min_pulls = min(total_featured_pull_counts)

    success_trials = sum(total_successes) / simulations
    successful_runs = total_successes.count(True)
    zero_success = total_successes.count(False)
    average_pulls_to_success = (
        sum(total_featured_pull_counts) / len(total_featured_pull_counts)
        if total_featured_pull_counts
        else None
    )
    median_pulls_to_success = (
        statistics.median(total_featured_pull_counts)
        if total_featured_pull_counts
        else None
    )
    natural_featured_count = total_natural_featured.count(True)
    sparked_featured_count = total_sparked_featured.count(True)
    spark_rate = round(spark_count / simulations, 4)
    average_off_banner_3stars = round(sum(total_off_banner_3_stars) / simulations, 2)
    all_one_stars = sum(total_one_stars)
    all_two_stars = sum(total_two_stars)
    all_three_stars = sum(total_three_stars)
    average_one_stars = round(sum(total_one_stars) / simulations, 2)
    average_two_stars = round(sum(total_two_stars) / simulations, 2)
    average_three_stars = round(sum(total_three_stars) / simulations, 2)

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
        "spark_rate": spark_rate,
        "max_pulls": max_pulls,
        "min_pulls": min_pulls,
        "natural_featured_trials_count": natural_featured_count,
        "sparked_featured_trials_count": sparked_featured_count,
        "total_featured_obtained": natural_featured_count + sparked_featured_count,
        "average_off_banner_3stars": average_off_banner_3stars,
        "all_one_stars": all_one_stars,
        "all_two_stars": all_two_stars,
        "all_three_stars": all_three_stars,
        "average_one_stars": average_one_stars,
        "average_two_stars": average_two_stars,
        "average_three_stars": average_three_stars,
        "example_pull_log": example_pull_log,
    }
