import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.database import Base, get_db
import app.core.database as _db_module

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    Session = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with Session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(test_engine):
    Session = async_sessionmaker(bind=test_engine, expire_on_commit=False)

    async def override_get_db():
        async with Session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    # Patch both the dependency and the module-level AsyncSessionLocal
    # so background tasks also use the test DB
    original_session_local = _db_module.AsyncSessionLocal
    _db_module.AsyncSessionLocal = Session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
    _db_module.AsyncSessionLocal = original_session_local
