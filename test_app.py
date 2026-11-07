"""Historical smoke test retained for backwards-compatible manual execution."""
from app import app


def test_home_page_displays_correct_message():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to FarmFresh Tester!" in response.data
