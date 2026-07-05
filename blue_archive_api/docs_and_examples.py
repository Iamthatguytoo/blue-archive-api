doc_list = {
    "/": {
        "response_description": "Greets you and checks if its running, shows you directions, and credits for creator of the API and the source for data",
        "summary": "Basic landing page when searching for this API"
    },
    "keys": {
        "response_description": "Prints out a key that contains 'sk_' and another 32 characters after that",
        "summary": "Self serve endpoint to create keys"
    },
    "students": {
        "response_description": "Paginated list of students with their combat stats, equipment, affiliations, and terrain ratings", 
        "summary": "Search for specific students with their stats in game"
    },
    "gacha-calculate": {
        "response_description": "Returns the total number of pulls, spark eligibility, remaining pulls needed to spark, probability of obtaining the rate-up naturally, and probability of requiring a spark",
        "summary": "Calculate gacha pull probabilities and spark progress based on available pyroxene",
        "example": {
            "pyroxene": 24000, 
            "rate_up": 0.007
        }
    },
    "gacha-simulate": {
        "response_description": "Returns simulation statistics including success rate, average and median pulls to success, spark occurrences, rate-up acquisition count, off-banner 3-star averages, and overall pull distribution metrics",
        "summary": "Run Monte Carlo simulations to estimate gacha outcomes, spark frequency, and pull statistics",
        "example": {
            "simulations": 100,
            "pyroxene": 24000,
            "rate_up": 0.007,
            "rate_up_3_star": 0.03,
            "pity_threshold": 100,
            "spark_threshold": 200
        }
    },
    "analyze-pulls": {
        "response_description": "Returns the estimated number of pulls, required pyroxene, target confidence level, and associated risk category for obtaining the rate-up unit",
        "summary": "Calculate the pulls and pyroxene required to reach a target probability of obtaining the rate-up unit",
        "example": {
            "probability": 0.8,
            "rate_up": 0.007
        }
    }
}
tags_metadata = [
    {
        "name": "default",
        "description": "Basic endpoints for the API itself."
    },
    {
        "name": "keys",
        "description": "Endpoints for creating and managing API keys."
    },
    {
        "name": "students",
        "description": "Retrieve Blue Archive student information."
    },
    {
        "name": "gacha",
        "description": "Probability calculations, pull target analysis, and Monte Carlo simulations."
    }
]
