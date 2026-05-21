from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from app.models.models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token", auto_error=False)


class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None
    grade: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: Optional[str]
    display_name: Optional[str]
    grade: Optional[str]


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def require_user(
    user: Optional[User] = Depends(get_current_user),
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/auth/register", response_model=TokenResponse, status_code=201)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new user with email/password."""
    result = await db.execute(select(User).where(User.email == request.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    user = User(
        email=request.email,
        hashed_password=get_password_hash(request.password),
        display_name=request.display_name,
        grade=request.grade,
        auth_provider="local",
    )
    db.add(user)
    await db.flush()

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/auth/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Obtain JWT tokens with email + password."""
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(refresh: str, db: AsyncSession = Depends(get_db)):
    """Refresh access token using a refresh token."""
    payload = decode_token(refresh)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="유효하지 않은 갱신 토큰입니다.")
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")

    access_token = create_access_token({"sub": user.id})
    new_refresh = create_refresh_token({"sub": user.id})
    return TokenResponse(access_token=access_token, refresh_token=new_refresh)


@router.get("/auth/me", response_model=UserResponse)
async def me(user: User = Depends(require_user)):
    """Get current user info."""
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        grade=user.grade,
    )
