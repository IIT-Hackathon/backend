from fastapi.testclient import TestClient
from ..main import app
from random import randrange
import pytest
from fastapi import status

ENDPOINT = "http://127.0.0.1:8000"

client = TestClient(app)

@pytest.mark.parametrize(
    "path,method",
    [
        (f"{ENDPOINT}/users", "POST"),
        (f"{ENDPOINT}/profile", "GET"),
        (f"{ENDPOINT}/login", "POST"),
    ],
)
def test_route_exists(path: str, method: str) -> None:
    """
    Test if the specified route exists and is reachable.
    """
    response = client.request(method, path)
    assert response.status_code not in (
        status.HTTP_404_NOT_FOUND,
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )

def generate_user() :
    random_number = randrange(1, 100000)
    return {
        "name" : "Fahim Shakil",
        "email": f"test@example{random_number}.com",
        "password": "password123",
        "phone" : "01913235951"
    }


def test_create_user():
    user_data = generate_user()
    response = client.post(ENDPOINT + "/users", json = user_data)
    assert response.status_code == 201
    user = response.json()
    assert user["access_token"] != None

def test_get_user_profile():
    user_data = generate_user()
    response = client.post(ENDPOINT + "/users", json = user_data)
    assert response.status_code == 201
    user = response.json()
    assert user["email"] == user_data["email"]
    
    


    


