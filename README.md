# AI Resume Ranker

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)

**An AI-powered resume ranking system** that evaluates candidates against a job description using a **hybrid scoring engine** combining semantic similarity, structured skill weighting, and keyword relevance.

This project is a **transparent and explainable** alternative to black-box ATS systems.

## Overview

AI Resume Ranker analyzes resumes against a given job description and produces:

- A **final candidate score** (0–100)
- Semantic similarity score
- Skill match score
- Keyword relevance score
- **Structured reasoning** explaining strengths, weaknesses, and missing skills

The goal is **not just ranking** , but clearly explaining **why** a candidate received that score.

## Architecture & Final Score Formula

```python
final_score = (
    0.5 * semantic_score +
    0.35 * skill_score +
    0.15 * keyword_score
)
```
This weighted combination ensures both deep contextual understanding and precise requirement matching.
Features

Resume ranking against any custom job description
Detailed structured reasoning for every candidate
Weighted skill extraction powered by LLM
Transparent, fully explainable scoring breakdown
Beautiful Streamlit frontend for quick testing
Clean, modular FastAPI backend

Project Structure
```bash
ai-resume-ranker/
├── app/
│   ├── llm.py              # LLM integration (OpenRouter)
│   ├── scoring.py          # Final score computation
│   ├── skill_scoring.py    # Skill-based scoring logic
│   ├── embedding.py        # Semantic similarity
│   ├── keyword.py          # Keyword scoring
│   ├── explain.py          # Structured reasoning builder
│   └── main.py             # FastAPI entrypoint
├── streamlit_app.py        # Streamlit frontend
├── requirements.txt
├── .env.example
└── README.md
```

How to Run
1. Clone the repository
``` bash
git clone https://github.com/ShirishAcharya/ai-resume-ranker.git
cd ai-resume-ranker
```
2. Create virtual environment
``` bash
python -m venv venv
```
Linux/macOS
``` bash
source venv/bin/activate
```
Windows
``` bash
venv\Scripts\activate
```
3. Install dependencies
``` bash
pip install -r requirements.txt
```
4. Add your API key
Create a .env file with this content:
```
OPENROUTER_API_KEY=sk-or-XXXXXXXXXXXXXXXX
```
5. Run backend
``` bash
uvicorn app.main:app --reload
```
6. Run frontend (in a new terminal)
``` bash
streamlit run streamlit_app.py
```
Open http://localhost:8501


Limitations


Experience extraction based on “X years” patterns has been disabled
LLM skill extraction may vary slightly between runs
Not intended for production hiring decisions without human validation
No bias mitigation layer yet

Why This Project
Most ATS tools give a score with zero explanation.
This system focuses on transparency, explainability, and structured reasoning.
