import os

import pytest
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orbify_projects.api.dependencies import get_session
from orbify_projects.db.base import Base
from orbify_projects.main import app

TEST_DATABASE_FILE = "test.db"
TEST_DATABASE_URI = f"sqlite:///{TEST_DATABASE_FILE}"


@pytest.fixture(scope="session")
def db_engine():
    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)

    engine = create_engine(TEST_DATABASE_URI, connect_args={"check_same_thread": False})
    yield engine

    if os.path.exists(TEST_DATABASE_FILE):
        os.remove(TEST_DATABASE_FILE)


@pytest.fixture(scope="session")
def db_setup(db_engine):
    Base.metadata.create_all(bind=db_engine)

    yield

    Base.metadata.drop_all(bind=db_engine)


@pytest.fixture(scope="session")
def db_session(db_engine, db_setup):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    async def mock_get_session():
        yield session

    app.dependency_overrides[get_session] = mock_get_session

    yield session


@pytest.fixture(scope="session")
def faker():
    yield Faker()
