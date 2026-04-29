from pydantic import BaseModel
from typing import List, Optional


class RankRequest(BaseModel):
    job_description: str
    resumes: List[str]


class RankedResume(BaseModel):
    name: str
    final_score: float
    semantic_score: float
    skill_score: float
    keyword_score: float
    reasoning: Optional[str] = None
    preview: str


class RankResponse(BaseModel):
    ranked_resumes: List[RankedResume]