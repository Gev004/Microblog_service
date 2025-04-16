import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.fixture
def headers():
    return {"api-key": "valid_api_key"}

def test_create_tweet_empty_content(headers):
    response = client.post("/api/tweets", json={"tweet_data": ""}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Tweet data cannot be empty"

def test_create_tweet_success(headers, mocker):
    mocker.patch("app.api_key_checking", return_value=mocker.Mock(id=1))
    mock_db = mocker.Mock()
    tweet_data = {"tweet_data": "Hello!", "tweet_media_ids": []}
    response = client.post("/api/tweets", json=tweet_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["result"] is True

def test_get_my_profile(headers, mocker):
    mocker.patch("app.api_key_checking", return_value=mocker.Mock(id=1, username="tester"))
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200
