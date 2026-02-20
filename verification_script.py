from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Api chat nequi"}

def test_create_message():
    session_id = str(uuid.uuid4())
    response = client.post(
        "/api/messages/",
        json={"session_id": session_id, "content": "Hola Mundo", "sender": "user"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Hola Mundo"
    assert data["session_id"] == session_id
    assert "message_id" in data
    assert "timestamp" in data

def test_filter_bad_words():
    session_id = str(uuid.uuid4())
    response = client.post(
        "/api/messages/",
        json={"session_id": session_id, "content": "Este es un mensaje con una mala palabra", "sender": "user"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "****" in data["content"]    

def test_get_messages():
    session_id = str(uuid.uuid4())
    client.post(
        "/api/messages/",
        json={"session_id": session_id, "content": "Mensaje 1", "sender": "user"}
    )
    
    response = client.get(f"/api/messages/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["content"] == "Mensaje 1"

if __name__ == "__main__":
    try:
        test_read_main()
        print("test_read_main PASO")
        test_create_message()
        print("test_create_message PASO")
        test_filter_bad_words()
        print("test_filter_bad_words PASO")
        test_get_messages()
        print("test_get_messages PASO")
        print("TODAS LAS PRUEBAS PASARON")
    except Exception as e:
        print(f"TEST FALLO: {e}")
