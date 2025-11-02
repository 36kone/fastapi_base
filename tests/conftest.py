from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import get_db, Base
from app.models import User
from app.core.security import get_password_hash


# -----------------------------
# FACTORY
# -----------------------------
class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f'test_user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.name}@test.com')
    phone = factory.Sequence(lambda n: f'5551999999{n:03d}')
    password = factory.LazyAttribute(lambda obj: f'{obj.name}_password')
    role = "user"


# -----------------------------
# FIXTURE: Sessão de teste
# -----------------------------
@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Usa Base.metadata no lugar de table_registry
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)


# -----------------------------
# FIXTURE: Cliente FastAPI
# -----------------------------
@pytest.fixture
def client(session):
    def get_test_db():
        yield session

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


# -----------------------------
# CONTEXT MANAGER: Mock de tempo no banco
# -----------------------------
@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_handler)
    try:
        yield time
    finally:
        event.remove(model, "before_insert", fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# -----------------------------
# FIXTURE: Usuário
# -----------------------------
@pytest.fixture
def user(session):
    pwd = "test123"
    user = UserFactory(password=get_password_hash(pwd))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd
    return user


# -----------------------------
# FIXTURE: Outro usuário
# -----------------------------
@pytest.fixture
def other_user(session):
    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# -----------------------------
# FIXTURE: Token de autenticação
# -----------------------------
@pytest.fixture
def token(client, user):
    response = client.post(
        "api/auth/login",
        data={"username": user.email, "password": user.clean_password},
    )
    data = response.json()
    return data.get("access_token")
