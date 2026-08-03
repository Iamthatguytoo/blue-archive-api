import random


def pull_spark(
    three_star_pity_count: int,
    pull_count: int,
    spark_threshold: int,
    pity_threshold: int,
    featured_rate: float,
    three_star_rate: float,
):
    success = False
    natural_featured = False
    spark = False
    off_banner = 0
    rarity = 0
    two_star_rate = 0.215
    roll = random.random()

    if pull_count >= spark_threshold:
        success = True
        spark = True
        rarity = 3

    elif three_star_pity_count >= pity_threshold or roll < three_star_rate:
        three_star_pity_count = 0

        if random.random() < (featured_rate / three_star_rate):
            success = True
            natural_featured = True
        else:
            off_banner = 1
        rarity = 3

    elif roll < two_star_rate:
        rarity = 2

    else:
        rarity = 1

    return {
        "success": success,
        "natural_featured": natural_featured,
        "spark": spark,
        "off_banner": off_banner,
        "three_star_pity_count": three_star_pity_count,
        "rarity": rarity,
    }

def pull_pity(
    three_star_pity_count: int,
    banner_pity: int,
    pity_threshold: int,
    featured_rate: float,
    three_star_rate: float,
):
    success = False
    natural_featured = False
    off_banner = 0
    rarity = 0
    two_star_rate = 0.215
    roll = random.random()

    if banner_pity >= 200:
        three_star_pity_count = 0
        success = True
        rarity = 3
        banner_pity = 0
    
    elif banner_pity == 100:
        three_star_pity_count = 0
        rarity = 3
        if random.random() < 0.5:
            natural_featured = True
            success = True
            banner_pity = 0
        else:
            off_banner = 1

    elif three_star_pity_count >= pity_threshold or roll < three_star_rate:
        three_star_pity_count = 0

        if random.random() < (featured_rate / three_star_rate):
            success = True
            natural_featured = True
            banner_pity = 0
        else:
            off_banner = 1
        rarity = 3

    elif roll < two_star_rate:
        rarity = 2

    else:
        rarity = 1

    return {
        "success": success,
        "natural_featured": natural_featured,
        "off_banner": off_banner,
        "banner_pity": banner_pity,
        "three_star_pity_count": three_star_pity_count,
        "rarity": rarity,
    }