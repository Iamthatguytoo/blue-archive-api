import random


def pull_spark(
    three_star_pity_count: int,
    pull_count: int,
    spark_threshold: int,
    pity_threshold: int,
    rate_up: float,
    rate_up_3_star: float,
):
    success = False
    rate_up_natural = False
    spark = False
    off_banner = 0
    rarity = 0
    two_star_rate = 0.215
    roll = random.random()

    if pull_count >= spark_threshold:
        success = True
        spark = True
        rarity = 3

    elif three_star_pity_count >= pity_threshold or roll < rate_up_3_star:
        three_star_pity_count = 0

        if random.random() < (rate_up / rate_up_3_star):
            success = True
            rate_up_natural = True
        else:
            off_banner = 1
        rarity = 3

    elif roll < two_star_rate:
        rarity = 2

    else:
        rarity = 1

    return {
        "success": success,
        "rate_up_natural": rate_up_natural,
        "spark": spark,
        "off_banner": off_banner,
        "three_star_pity_count": three_star_pity_count,
        "rarity": rarity,
    }
