import math

def calculate_gacha(pyroxene: int, rate_up: float):
    pulls = pyroxene // 120
    fail_prob = math.pow(1 - rate_up, pulls)
    success_prob = 1 - fail_prob
    pulls_to_spark = max(200 - pulls, 0)

    return {
        "pulls": pulls,
        "spark_reachable":pulls >= 200,
        "pulls_to_spark": pulls_to_spark,
        "chance_get_rate_up_naturally": round(success_prob * 100, 6),
        "chance_need_spark": round(fail_prob * 100, 6)
    }