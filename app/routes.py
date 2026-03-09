from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from app.services.parser import parse_pdf, parse_docx
from app.services.ranking import rank_resumes
from schemas import RankResponse, RankedResume

router = APIRouter()

@router.post("/rank", response_model=RankResponse)
async def rank(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    parsed_resumes = []

    for file in files:
        content = await file.read()
        if file.filename.endswith(".pdf"):
            text = parse_pdf(content)
        elif file.filename.endswith(".docx"):
            text = parse_docx(content)
        else:
            continue

        parsed_resumes.append(text)

    ranked = rank_resumes(job_description, parsed_resumes)

    response = [
        RankedResume(
            final_score=r["final_score"],
            semantic_score=r["semantic_score"],
            skill_score=r["skill_score"],
            keyword_score=r["keyword_score"],
            experience_score=r["experience_score"],
            reasoning=r["reasoning"],
            preview=r["resume"][:300]
        )
        for r in ranked
    ]

    return RankResponse(ranked_resumes=response)