"""Historical Flask route tests, repaired for the actual application."""
import pytest
from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to FarmFresh Tester!" in response.data


def test_products_page(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert b"Our Products" in response.data


def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"About FarmFresh Tester" in response.data
