from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_function_filter():
    response = client.post(
        "/filter/case_sensitive",
        headers={"X-Token": "coneofsilence"},
        data = '["Мама", "МАМА", "Мама", "папа", "ПАПА", "ДЯдя", "брАт", "Дядя", "Дядя"]'
    )
    print(response)
    assert response.status_code == 200
    assert response.json() == [
            "папа",
            "брат"
          ]
