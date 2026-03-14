import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "dup@mergington.edu"})
    # Duplicate signup
    response = client.post("/activities/Programming Class/signup", params={"email": "dup@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_signup_full():
    # Fill up activity
    for i in range(12):
        client.post("/activities/Chess Club/signup", params={"email": f"full{i}@mergington.edu"})
    response = client.post("/activities/Chess Club/signup", params={"email": "overflow@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"

def test_signup_nonexistent():
    response = client.post("/activities/Nonexistent/signup", params={"email": "ghost@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
