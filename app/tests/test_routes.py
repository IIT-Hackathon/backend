from fastapi.testclient import TestClient
from ..main import app
from random import randrange
import pytest
from fastapi import status
from dotenv import load_dotenv
import os 

load_dotenv()

ENDPOINT = "http://localhost:8000"

client = TestClient(app)

@pytest.mark.parametrize(
    "path,method",
    [
        (f"{ENDPOINT}/users", "POST"),
        (f"{ENDPOINT}/profile", "GET"),
        (f"{ENDPOINT}/users/{id}", "DELETE"),
        (f"{ENDPOINT}/login", "POST"),
        (f"{ENDPOINT}/new_tax", "POST"),
        (f"{ENDPOINT}/reports", "GET"),
        (f"{ENDPOINT}/current_report", "GET"),
        (f"{ENDPOINT}/tax_info", "GET"),
        (f"{ENDPOINT}/tax_info", "PUT"),
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
        "name": "Fahim Shakil",
        "email": f"user{random_number}@example.com",
        "password": "1234",
        "dob": "1980-11-03",
        "gender": "male",
        "city": "dhaka"
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
    token = response.json()["access_token"]
    profile = client.get(ENDPOINT + "/profile", headers={"Authorization": f"Bearer {token}"})
    assert profile.status_code == 200
    
    
def test_update_user_profile() :
    user_data = generate_user()
    response = client.post(ENDPOINT + "/users", json = user_data)
    token = response.json()["access_token"]
    new_user_data = {
        "name" : "different name",
        "age": 0,
        "gender": "male",
        "city": "chattogram"
    }
    response2 = client.put(ENDPOINT + "/users", json = new_user_data, headers={"Authorization": f"Bearer {token}"})
    assert response2.status_code == 200
    final_response = response2.json()
    assert final_response["response"] == "successful"
    
def test_new_tax_added() :
    user_data = generate_user()
    response = client.post(ENDPOINT + "/users", json = user_data)
    token = response.json()["access_token"]
    tax_data = {
        "year" : 2021,
        "income" : 100000,
        "city" : "dhaka"
    }
    response2 = client.post(ENDPOINT + "/new_tax", json = tax_data, headers={"Authorization": f"Bearer {token}"})
    assert response2.status_code == 200
    final_response = response2.json()
    assert final_response["tax"] == 0
    
def test_get_tax_reports() :
    user_data = generate_user()
    response = client.post(ENDPOINT + "/users", json = user_data)
    token = response.json()["access_token"]
    tax_data = {
        "year" : 2021,
        "income" : 100000,
        "city" : "dhaka"
    }
    response2 = client.post(ENDPOINT + "/new_tax", json = tax_data, headers={"Authorization": f"Bearer {token}"})
    response3 = client.get(ENDPOINT + "/reports", headers={"Authorization": f"Bearer {token}"})
    assert response3.status_code == 200
    final_response = response3.json()
    assert len(final_response) > 0
    
def test_get_current_tax_report() :
    user_data = generate_user()
    response = client.post(ENDPOINT + "/users", json = user_data)
    token = response.json()["access_token"]
    tax_data = {
        "year" : 2021,
        "income" : 100000,
        "city" : "dhaka"
    }
    response2 = client.post(ENDPOINT + "/new_tax", json = tax_data, headers={"Authorization": f"Bearer {token}"})
    response3 = client.get(ENDPOINT + "/current_report", params = {"year" : 2021}, headers={"Authorization": f"Bearer {token}"})
    assert response3.status_code == 200

    
def test_update_tax_info() :
    user_data = generate_user()
    response = client.post(ENDPOINT + "/users", json = user_data)
    token = response.json()["access_token"]
    tax_data = {
        "year" : 2021,
        "income" : 100000,
        "city" : "dhaka"
    }
    response2 = client.post(ENDPOINT + "/new_tax", json = tax_data, headers={"Authorization": f"Bearer {token}"})
    tax_info = {
        "income" : 200000,
        "city" : "chattogram"
    }
    response3 = client.put(ENDPOINT + "/tax_info", json = tax_info, headers={"Authorization": f"Bearer {token}"})
    assert response3.status_code == 200





    

    
    


    


