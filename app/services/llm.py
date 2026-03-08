import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL="meta-llama/llama-3-8b-instruct"

def extract_weighted_skills(job_description: str) -> dict:
    prompt = f"""
                Extract the top backend engineering skills from the job description below.

                Return ONLY a valid JSON dictionary.
                Do not include explanation.
                Do not include markdown.
                Do not include backticks.

                Format:
                {{
                "Python": 0.9,
                "FastAPI": 0.8
                }}

                Weights must be between 0 and 1.

                Job Description:
                {job_description}
            """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except:
        return {}
    

def generate_reasoning(job_description: str, resume_text: str):
    prompt = f"""
                You are a hiring assistant.

                Explain briefly why this candidate is a good or weak fit.
                Mention missing critical skills if any.
                Keep under 120 words.

                Job Description:
                {job_description}

                Resume:
                {resume_text[:3000]}

                Always format reasoning as:
                - Candidate Fit:
                - Strengths:
                - Weaknesses:
                - Missing Critical Skills:
                            """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()