from fastapi import FastAPI
from app.routes import router

app = FastAPI(title = "Resume Ranker using AI")

app.include_router(router)

@app.get("/")
async def get_status():
    return{"Welcome to Resume Ranker"}