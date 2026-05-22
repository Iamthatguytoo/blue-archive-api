import math

def pull_target(probability: float, rate_up: float):
    pulls = math.log(1 - probability) / math.log(1 - rate_up)
    pulls = int(math.ceil(pulls))

    pyroxene = pulls * 120

    return {
        "required_pulls": pulls,
        "pyroxene_needed": pyroxene,
        "confidence": probability,
        "risk_level": (
            "low" if probability >= 0.9 else
            "moderate" if probability >= 0.7 else
            "high"
        )
    }