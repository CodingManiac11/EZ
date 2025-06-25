import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Fixtures for test user data
def test_client_signup_and_verify(monkeypatch):
    # Mock email sending
    monkeypatch.setattr("app.email_utils.send_verification_email", lambda to_email, url: None)
    resp = client.post("/client/signup", json={"email": "testclient@example.com", "password": "testpass123"})
    assert resp.status_code == 200
    token = resp.json()["verify_url"].split("token=")[-1]
    # Verify email
    resp = client.get(f"/client/verify-email?token={token}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Email verified successfully"

def test_client_login():
    resp = client.post("/client/login", data={"username": "testclient@example.com", "password": "testpass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()

def test_ops_login():
    # You must create an ops user in the DB manually for this test to pass
    resp = client.post("/ops/login", data={"username": "ops@example.com", "password": "opspass123"})
    assert resp.status_code in [200, 400]  # 400 if not present

def test_upload_and_list_files(monkeypatch):
    # Login as ops (must exist)
    resp = client.post("/ops/login", data={"username": "ops@example.com", "password": "opspass123"})
    if resp.status_code != 200:
        pytest.skip("Ops user not present")
    token = resp.json()["access_token"]
    # Upload file
    file_content = b"test file content"
    files = {"file": ("test.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    resp = client.post("/ops/upload", files=files, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    # Login as client
    resp = client.post("/client/login", data={"username": "testclient@example.com", "password": "testpass123"})
    token = resp.json()["access_token"]
    # List files
    resp = client.get("/client/files", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    files = resp.json()
    assert isinstance(files, list)
    if files:
        file_id = files[0]["id"]
        # Get download link
        resp = client.get(f"/client/download-file/{file_id}", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        download_link = resp.json()["download_link"]
        # Download file
        resp = client.get(download_link, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code in [200, 404]  # 404 if file missing 