import io
import os

def test_create_tweet(client, test_user):
    response = client.post(
        "/api/tweets",
        headers={"api-key": test_user.api_key},
        json={"tweet_data": "Hello world", "tweet_media_ids": []}
    )
    assert response.status_code == 200
    assert response.json()["result"] is True

def test_upload_media(client, test_user):
    file_content = b"fake image content"
    file = io.BytesIO(file_content)

    response = client.post(
        "/api/medias",
        headers={"api-key": test_user.api_key},
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 200
    assert "media_id" in response.json()

def test_like_unlike_tweet(client, test_user, db):
    tweet_res = client.post(
        "/api/tweets",
        headers={"api-key": test_user.api_key},
        json={"tweet_data": "test like", "tweet_media_ids": []}
    )
    tweet_id = tweet_res.json()["tweet_id"]

    like_res = client.post(f"/api/tweets/{tweet_id}/likes", headers={"api-key": test_user.api_key})
    assert like_res.status_code == 200
    assert like_res.json()["result"]

    unlike_res = client.delete(f"/api/tweets/{tweet_id}/remove_likes", headers={"api-key": test_user.api_key})
    assert unlike_res.status_code == 200
    assert unlike_res.json()["result"]

def test_follow_unfollow(client, db, test_user):
    other_user = User(username="another", api_key="otherkey")
    db.add(other_user)
    db.commit()

    follow_res = client.post(f"/api/tweets/{other_user.id}/follow", headers={"api-key": test_user.api_key})
    assert follow_res.status_code == 200
    assert "message" in follow_res.json()

    unfollow_res = client.delete(f"/api/tweets/{other_user.id}/unfollow", headers={"api-key": test_user.api_key})
    assert unfollow_res.status_code == 200
    assert "message" in unfollow_res.json()

def test_get_timeline(client, test_user):
    res = client.get("/api/tweets", headers={"api-key": test_user.api_key})
    assert res.status_code == 200
    assert res.json()["result"] is True

def test_get_my_profile(client, test_user):
    res = client.get("/api/users/me", headers={"api-key": test_user.api_key})
    assert res.status_code == 200
    assert res.json()["result"] is True
    assert res.json()["user"]["name"] == test_user.username

def test_get_user_profile(client, db, test_user):
    another = User(username="another2", api_key="anotherkey")
    db.add(another)
    db.commit()
    res = client.get(f"/api/users/{another.id}")
    assert res.status_code == 200
    assert res.json()["result"] is True
