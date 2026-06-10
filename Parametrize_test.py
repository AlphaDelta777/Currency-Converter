def grade(score: int) -> str:
    """
    Return letter grade for a numeric score 0-100.
    Raises ValueError for negative numbers, numbers > 100, and letters.
    """

    if not isinstance(score, (int, float)) or isinstance(score, bool):
        raise ValueError("Score must be a numeric value.")

    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")
        
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"