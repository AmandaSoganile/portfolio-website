import pytest
from app import create_app
from store import Store


@pytest.fixture
def app():
    return create_app({
        "TESTING": True,
        "DATABASE": ":memory:",
        "STORAGE_BACKEND": "sqlite",
    })


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def store():
    return Store(":memory:")
