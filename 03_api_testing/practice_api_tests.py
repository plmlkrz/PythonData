# MODULE 3 — PRACTICE: reproduce the API test file from memory.
#
# SETUP:
#   BASE_URL = "https://jsonplaceholder.typicode.com"
#
# FIXTURES:
#   - session()  — module-scoped requests.Session, closed on teardown
#
# TESTS TO WRITE:
#   GET /posts/1
#     - returns 200
#     - json has keys: id, title, body, userId
#     - id equals 1
#   GET /posts/99999
#     - returns 404
#   GET /posts
#     - returns list of 100
#     - filtering by userId works (all results share that userId)
#   POST /posts  (payload: title, body, userId)
#     - returns 201
#     - response contains an id (int)
#     - response echoes the payload values
#   Headers
#     - Content-Type contains "application/json"
#   Schema check
#     - every post in /posts has all required keys
#
# Write your code below.
# ─────────────────────────────────────────────────────────────────────────────
import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

# Fixtures

@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    yield s
    s.close()

#GET

def test_get_post_returns_200(session):
    response = session.get(f"{BASE_URL}/post/1")
    assert response.status_code == 200

def test_get_post_json_structure(session):
    response = session.get(f"{BASE_URL}/post/1")
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "body" in data
    assert "userid" in data

def test_get_post_correct_id(session):
    response = session.get(f"{BASE_URL}/post/1")
    data = response.json()
    assert data["id"] == 1

def test_get_nonexistent_post_returns_404(session):
    response = session.get(f"{BASE_URL}/post/999999")
    assert response.status_code == 404

# Get - read a collection

def test_get_all_post_returns_list(session):
    response = session.get(f"{BASE_URL}/post")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100

def test_get_post_by_user(session):
    response = session.get(f"{BASE_URL}/posts", params={"userId": 1})
    data = response.json()
    assert all(post["userid"] == 1 for post in data)


# POST - Create a resource

def test_create_post_returns_201(session):
    payload = {"title" : "Test Song", "body" : "royalty data", "userId": 1}
    response = session.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201

def test_create_post_response_contains_id(session):
    payload = {"title" : "Test Song", "body" : "royalty data", "userId": 1}
    response = session.post(f"{BASE_URL}/posts", json=payload)
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)

def test_create_post_echoes_payload(session):
    payload = {"title" : "Test Song", "body": "My Body", "userId" : 42 }
    response = session.post(f"{BASE_URL}/posts", json=payload)
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]

# Response Headers

def test_response_content_type_json(session):
    response = session.get(f"{BASE_URL}/posts/1")
    assert "application/json" in response.headers["Content-Type"]

#Helper Pattern

REQUIRED_POST_KEYS = {"id", "title", "body", "userId"}
def test_all_posts_have_required_keys(session):
    response = session.get(f"{BASE_URL}/posts")
    posts = response.json()
    for post in posts:
        missing = REQUIRED_POST_KEYS - set(post.keys())
        assert not missing, f"post {post.get("id")} missing keys: {missing}"


