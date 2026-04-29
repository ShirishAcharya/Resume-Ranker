import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "meta-llama/llama-3-8b-instruct"


def extract_weighted_skills(job_description: str) -> dict:
    prompt = f"""
You are a technical recruiter. Extract the most important skills and qualifications 
from the job description below.

Return ONLY a valid JSON dictionary where:
- Keys are skill names (e.g. "Python", "React", "Project Management")
- Values are importance weights between 0.0 and 1.0 (1.0 = absolutely critical)

Rules:
- Do NOT include markdown, backticks, or explanation
- Do NOT assume a specific domain — derive everything from the job description
- Include both technical and soft skills if mentioned
- Return between 5 and 15 skills

Example format:
{{"Python": 0.9, "REST APIs": 0.8, "Communication": 0.5}}

Job Description:
{job_description}
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        skills = json.loads(content)
        return {
            k: max(0.0, min(1.0, float(v)))
            for k, v in skills.items()
            if isinstance(k, str)
        }
    except (json.JSONDecodeError, ValueError):
        return {}

def generate_reasoning(job_description: str, resume_text: str) -> str:
    prompt = f"""
You are a hiring assistant. Evaluate this candidate against the job description.
Be concise and specific. Keep your response under 120 words.

Always use exactly this format:
- Candidate Fit: (overall fit in one sentence)
- Strengths: (what the candidate does well for this role)
- Weaknesses: (gaps or concerns)
- Missing Critical Skills: (skills in the JD that are absent from the resume, or "None")

Job Description:
{job_description}

Resume:
{resume_text[:3000]}
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()