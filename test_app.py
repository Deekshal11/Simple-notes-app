
import pytest
from app import app, notes


@pytest.fixture
def client():
    app.config["TESTING"] = True
    notes.clear()

    with app.test_client() as client:
        yield client

    notes.clear()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Docker Notes App" in response.data


def test_add_note(client):
    response = client.post(
        "/add",
        data={"note": "Test note"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Test note" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_empty_note_is_not_added(client):
    client.post("/add", data={"note": "   "})
    assert notes == []
