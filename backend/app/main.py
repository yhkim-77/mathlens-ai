from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.api import analyze, problems, users, concepts
from app.api import auth, submissions


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="수학 풀이 인식 기반 AI 튜터 백엔드 API",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(analyze.router, prefix="/api/v1", tags=["analyze"])
app.include_router(problems.router, prefix="/api/v1", tags=["problems"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(concepts.router, prefix="/api/v1", tags=["concepts"])
app.include_router(submissions.router, prefix="/api/v1", tags=["submissions"])
# WebSocket router (no prefix for ws://)
app.include_router(submissions.router, tags=["websocket"])


@app.get("/")
def root():
    return {"message": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
