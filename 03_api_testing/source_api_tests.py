# MODULE 3 — API Testing with requests + pytest
# Uses JSONPlaceholder (free fake REST API) — no key needed.
# Install:  pip install requests pytest
# Run:      pytest 03_api_testing/source_api_tests.py -v
#
# KEY CONCEPTS:
#   - requests.get / post / put / delete
#   - response.status_code, response.json(), response.headers
#   - Asserting structure, types, and values of JSON responses
#   - A session fixture so every test reuses one HTTP session (faster)

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────

@pytest.fixture(scope="module")
def session():
    """One HTTP session shared across all tests in this module."""
    s = requests.Session()
    yield s
    s.close()


# ─────────────────────────────────────────
# GET — read a single resource
# ─────────────────────────────────────────

def test_get_post_returns_200(session):
    response = session.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200


def test_get_post_json_structure(session):
    response = session.get(f"{BASE_URL}/posts/1")
    data = response.json()

    assert "id" in data
    assert "title" in data
    assert "body" in data
    assert "userId" in data


def test_get_post_correct_id(session):
    response = session.get(f"{BASE_URL}/posts/1")
    data = response.json()
    assert data["id"] == 1


def test_get_nonexistent_post_returns_404(session):
    response = session.get(f"{BASE_URL}/posts/99999")
    assert response.status_code == 404


# ─────────────────────────────────────────
# GET — read a collection
# ─────────────────────────────────────────

def test_get_all_posts_returns_list(session):
    response = session.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100


def test_get_posts_by_user(session):
    response = session.get(f"{BASE_URL}/posts", params={"userId": 1})
    data = response.json()
    assert all(post["userId"] == 1 for post in data)


# ─────────────────────────────────────────
# POST — create a resource
# ─────────────────────────────────────────

def test_create_post_returns_201(session):
    payload = {"title": "Test Song", "body": "royalty data", "userId": 1}
    response = session.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201


def test_create_post_response_contains_id(session):
    payload = {"title": "Test Song", "body": "royalty data", "userId": 1}
    response = session.post(f"{BASE_URL}/posts", json=payload)
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)


def test_create_post_echoes_payload(session):
    payload = {"title": "My Title", "body": "My Body", "userId": 42}
    response = session.post(f"{BASE_URL}/posts", json=payload)
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]


# ─────────────────────────────────────────
# RESPONSE HEADERS
# ─────────────────────────────────────────

def test_response_content_type_is_json(session):
    response = session.get(f"{BASE_URL}/posts/1")
    assert "application/json" in response.headers["Content-Type"]


# ─────────────────────────────────────────
# HELPER PATTERN: validate schema of every item in a list
# ─────────────────────────────────────────

REQUIRED_POST_KEYS = {"id", "title", "body", "userId"}

def test_all_posts_have_required_keys(session):
    response = session.get(f"{BASE_URL}/posts")
    posts = response.json()
    for post in posts:
        missing = REQUIRED_POST_KEYS - set(post.keys())
        assert not missing, f"Post {post.get('id')} missing keys: {missing}"
