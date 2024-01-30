from fastapi.testclient import TestClient
from starlette import status

from main import app

client = TestClient(app)


def test_user_details():
    response = client.get("/user/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"user_id": 1, "name": "John Doe"}

    response = client.get("/user/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}