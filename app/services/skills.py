import re 

def compute_skill_score(resume_text: str, weighted_skills: dict) -> float:
    if not weighted_skills:
        return 0.0

    total_weight = sum(weighted_skills.values())
    matched_weight = 0

    resume_lower = resume_text.lower()
    resume_words = set(re.findall(r'\b\w+\b', resume_lower))


    for skill, weight in weighted_skills.items():
        skill_words = set(skill.lower().split())
        if skill_words & resume_words:
            matched_weight += weight

    return matched_weight / total_weight if total_weight > 0 else 0.0