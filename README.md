# Resume Ranker

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)

An AI-powered resume ranking system that evaluates candidates against a job description using a hybrid scoring engine — combining semantic similarity, structured skill weighting, and keyword relevance.

Built as a transparent alternative to black-box ATS systems, where candidates actually get to see *why* they ranked where they did.

## Overview

Resume Ranker takes a job description and a set of resumes, then produces:

- A **final candidate score** (0–1)
- Semantic similarity score
- Skill match score
- Keyword relevance score
- Candidate name extracted from the resume
- Matched skills list
- Structured reasoning covering strengths, weaknesses, and missing skills (for top candidates)

The goal isn't just to rank — it's to explain the ranking in a way that's actually useful.

## Scoring Formula

```python
final_score = (
    0.5 * semantic_score +
    0.35 * skill_score +
    0.15 * keyword_score
)
```

Semantic similarity carries the most weight since it captures contextual fit beyond just keyword matching. Skill score uses LLM-extracted weighted skills from the job description, so it adapts to any role — not just engineering. Keyword score acts as a lightweight tiebreaker.

## Features

- Works with any job description — not hardcoded to a specific domain
- Extracts candidate names automatically from uploaded resumes
- Shows which skills from the JD were matched in each resume
- LLM-generated structured reasoning for top-ranked candidates
- Fully explainable scoring breakdown
- Streamlit frontend for quick testing
- Modular FastAPI backend

## Project Structure

```bash
resume-ranker/
├── app/
│   ├── services/
│   │   ├── llm.py          # Skill extraction and reasoning via LLM
│   │   ├── ranking.py      # Core scoring logic
│   │   ├── skills.py       # Skill matching utilities
│   │   ├── embedding.py    # Sentence embeddings and cosine similarity
│   │   └── parser.py       # PDF and DOCX parsing + name extraction
│   └── routes.py           # FastAPI route definitions
├── streamlit_app.py        # Streamlit frontend
├── main.py                 # FastAPI entrypoint
├── schemas.py              # Pydantic models
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

## How to Run

1. Clone the repository

```bash
git clone https://github.com/ShirishAcharya/ai-resume-ranker.git
cd ai-resume-ranker
```

2. Create and activate a virtual environment

```bash
python -m venv venv
```

Linux/macOS
```bash
source venv/bin/activate
```

Windows
```bash
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up your API key

Get a free key from [OpenRouter](https://openrouter.ai) and create a `.env` file:

```
OPENROUTER_API_KEY=sk-or-XXXXXXXXXXXXXXXX
```
5. Run the backend

```bash
uvicorn main:app --reload
```

6. Run the frontend (in a separate terminal)

```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501

## Limitations

- Name extraction relies on the first line of the resume being the candidate's name, which is true for most standard formats but may not always hold
- LLM skill extraction can vary slightly between runs due to model temperature
- Not intended for production hiring decisions without human review
- No bias mitigation layer

## Why This Project

Most ATS tools hand you a score and call it a day. This project started from the frustration of not knowing *why* a resume got ranked the way it did — so the focus here was always on transparency and structured reasoning over just the number.
