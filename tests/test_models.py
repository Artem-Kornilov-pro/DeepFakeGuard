"""Tests for database models."""

from __future__ import annotations

import uuid
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.api.models import Base, FederatedClient, FederatedRound, InferenceTask, User


@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """Create an async in-memory SQLite session for testing."""
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession) -> None:
    """Test creating a User record."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_secret",
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "user"
    assert user.is_active is True
    assert user.created_at is not None


@pytest.mark.asyncio
async def test_create_federated_client(async_session: AsyncSession) -> None:
    """Test creating a FederatedClient record."""
    client = FederatedClient(
        client_id="client-001",
        name="Test Client",
        total_samples=100,
    )
    async_session.add(client)
    await async_session.commit()
    await async_session.refresh(client)

    assert client.id is not None
    assert client.client_id == "client-001"
    assert client.name == "Test Client"
    assert client.total_samples == 100
    assert client.is_active is True


@pytest.mark.asyncio
async def test_create_inference_task(async_session: AsyncSession) -> None:
    """Test creating an InferenceTask with a linked User."""
    user = User(
        username="taskuser",
        email="task@example.com",
        hashed_password="hashed_secret",
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    task = InferenceTask(
        user_id=user.id,
        video_path="/videos/test.mp4",
        status="pending",
    )
    async_session.add(task)
    await async_session.commit()
    await async_session.refresh(task)

    assert task.id is not None
    assert task.user_id == user.id
    assert task.status == "pending"
    assert task.prediction is None
    assert task.confidence is None


@pytest.mark.asyncio
async def test_create_federated_round(async_session: AsyncSession) -> None:
    """Test creating a FederatedRound record."""
    round_obj = FederatedRound(
        round_number=1,
        status="started",
        participants_count=5,
    )
    async_session.add(round_obj)
    await async_session.commit()
    await async_session.refresh(round_obj)

    assert round_obj.id is not None
    assert round_obj.round_number == 1
    assert round_obj.status == "started"
    assert round_obj.participants_count == 5
    assert round_obj.global_metrics is None
