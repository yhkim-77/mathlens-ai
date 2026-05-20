from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze, problems, users, concepts

app = FastAPI(
    title="MathLens AI API",
    description="수학 풀이 인식 기반 AI 튜터 백엔드 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])
app.include_router(problems.router, prefix="/api/v1", tags=["problems"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(concepts.router, prefix="/api/v1", tags=["concepts"])


@app.get("/")
def root():
    return {"message": "MathLens AI API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
