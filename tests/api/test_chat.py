from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_chat_no_documents():
    client.post("/reset")
    response = client.post("/chat", json={"query": "What is this document about?"})
    assert response.status_code == 200
    json_response = response.json()
    assert "answer" in json_response


def test_chat_with_documents():
    # Assume documents are uploaded in a previous test
    response = client.post("/chat", json={"query": "Summarize the content of the uploaded doc."})
    assert response.status_code == 200
    json_response = response.json()
    assert "answer" in json_response


def test_reset():
    client.post("/chat", json={"query": "Remember this information."})
    reset_response = client.post("/reset")
    assert reset_response.status_code == 200
    follow_up = client.post("/chat", json={"query": "What did you remember?"})
    json_followup = follow_up.json()
    assert "answer" in json_followup
