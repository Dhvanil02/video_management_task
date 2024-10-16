import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_video():
    with open("test_video.mp4", "rb") as video:
        response = client.post("/upload/", files={"file": video})
    assert response.status_code == 200

def test_search_video():
    response = client.get("/search/?name=test")
    assert response.status_code == 200

def test_block_video():
    response = client.get("/video/blocked_video_id1")
    assert response.status_code == 403
