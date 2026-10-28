
import pytest
from app import app, init_db


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["DATABASE"] = str(tmp_path / "test_notes.db")

    init_db()

    with app.test_client() as client:
        yield client


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
    response = client.get("/")
    assert b"No notes yet" in response.data


def test_note_persists_between_requests(client):
    client.post("/add", data={"note": "Persistent note"})

    response = client.get("/")
    assert b"Persistent note" in response.data
