from app.services.embedding import get_embedding, cosine_similarity
from app.services.llm import extract_weighted_skills, generate_reasoning
from app.services.skills import compute_skill_score

SEMANTIC_WEIGHT = 0.5
SKILL_WEIGHT = 0.35
KEYWORD_WEIGHT = 0.15

def compute_keyword_score(resume_text: str, job_description: str):
    jd_keywords = set(job_description.lower().split())
    resume_words = set(resume_text.lower().split())

    if not jd_keywords:
        return 0.0

    hits = len(jd_keywords.intersection(resume_words))
    return hits / len(jd_keywords)


def rank_resumes(job_description: str, resumes: list[str], explain_top_n: int = 3):

    weighted_skills = extract_weighted_skills(job_description)
    jd_embedding = get_embedding(job_description)

    results = []

    for resume in resumes:
        semantic_score = cosine_similarity(
            jd_embedding,
            get_embedding(resume)
        )

        skill_score = compute_skill_score(resume, weighted_skills)
        keyword_score = compute_keyword_score(resume, job_description)

        final_score = (
            semantic_score * SEMANTIC_WEIGHT +
            skill_score * SKILL_WEIGHT +
            keyword_score * KEYWORD_WEIGHT 
        )

        results.append({
            "resume": resume,
            "final_score": final_score,
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "keyword_score": keyword_score,
            "reasoning": None
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    for i in range(min(explain_top_n, len(results))):
        results[i]["reasoning"] = generate_reasoning(
            job_description,
            results[i]["resume"]
        )

    return results