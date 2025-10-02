import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.database import Base, get_db
from src.app import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = SessionTesting()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


def test_create_owner(client: TestClient):
    response = client.post(
        "/owners/",
        json={
            "name": "John Doe"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "pets": []}


def test_read_owners(client: TestClient):
    response = client.get("/owners/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_owner(client: TestClient):
    response = client.get("/owners/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Owner not found"}


def test_create_pet_for_owner(client: TestClient):
    client.post(
        "/owners/",
        json={
            "name": "John Doe"
        },
    )
    response = client.post(
        "/owners/1/pets/",
        json={
            "name": "Buddy",
            "species": "Dog"
        },
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Buddy",
                               "species": "Dog", "owner_id": 1}


def test_read_pets(client: TestClient):
    response = client.get("/pets/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_pet(client: TestClient):
    response = client.get("/pets/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pet not found"}
