def generate_decision(score: float, reasoning: str) -> dict:
    if score >= 0.75:
        return {
            "decision": "Shortlist",
            "confidence": 0.9
        }
    elif score >= 0.5:
        return {
            "decision": "Review",
            "confidence": 0.7
        }
    else:
        return {
            "decision": "Reject",
            "confidence": 0.8
        }