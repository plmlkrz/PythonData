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

import pytest  # Import pytest testing framework
import requests  # Import requests library for HTTP requests

BASE_URL = "https://jsonplaceholder.typicode.com"  # Define base URL for fake API (free test API)


# ─────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────

@pytest.fixture(scope="module")  # Create fixture with module scope (shared across all tests in this module)
def session():  # Fixture function: provides HTTP session for tests
    """One HTTP session shared across all tests in this module."""
    s = requests.Session()  # Create HTTP session (reuses connection, faster than new request each time)
    yield s  # Provide session to tests (they run here)
    s.close()  # Teardown: close session after all tests in module complete


# ─────────────────────────────────────────
# GET — read a single resource
# ─────────────────────────────────────────

def test_get_post_returns_200(session):  # Test that GET request returns success status
    response = session.get(f"{BASE_URL}/posts/1")  # Make GET request to fetch post with ID 1
    assert response.status_code == 200  # Assert HTTP status is 200 (OK)


def test_get_post_json_structure(session):  # Test that response has expected JSON structure
    response = session.get(f"{BASE_URL}/posts/1")  # Make GET request
    data = response.json()  # Parse response body as JSON

    assert "id" in data  # Assert "id" key exists in JSON
    assert "title" in data  # Assert "title" key exists
    assert "body" in data  # Assert "body" key exists
    assert "userId" in data  # Assert "userId" key exists


def test_get_post_correct_id(session):  # Test that response contains correct ID
    response = session.get(f"{BASE_URL}/posts/1")  # Make GET request
    data = response.json()  # Parse JSON response
    assert data["id"] == 1  # Assert the ID in response is 1


def test_get_nonexistent_post_returns_404(session):  # Test that requesting non-existent resource returns 404
    response = session.get(f"{BASE_URL}/posts/99999")  # Make GET request with invalid ID
    assert response.status_code == 404  # Assert HTTP status is 404 (Not Found)


# ─────────────────────────────────────────
# GET — read a collection
# ─────────────────────────────────────────

def test_get_all_posts_returns_list(session):  # Test that getting all posts returns a list
    response = session.get(f"{BASE_URL}/posts")  # Make GET request without ID (returns all posts)
    assert response.status_code == 200  # Assert HTTP status is 200
    data = response.json()  # Parse JSON response
    assert isinstance(data, list)  # Assert response is a list
    assert len(data) == 100  # Assert list contains 100 posts


def test_get_posts_by_user(session):  # Test filtering posts by userId parameter
    response = session.get(f"{BASE_URL}/posts", params={"userId": 1})  # GET with query parameter userId=1
    data = response.json()  # Parse JSON response
    assert all(post["userId"] == 1 for post in data)  # Assert all posts in response have userId == 1


# ─────────────────────────────────────────
# POST — create a resource
# ─────────────────────────────────────────

def test_create_post_returns_201(session):  # Test that POST request returns 201 (Created) status
    payload = {"title": "Test Song", "body": "royalty data", "userId": 1}  # Create request body
    response = session.post(f"{BASE_URL}/posts", json=payload)  # Make POST request with JSON payload
    assert response.status_code == 201  # Assert HTTP status is 201 (Created)


def test_create_post_response_contains_id(session):  # Test that POST response includes an ID
    payload = {"title": "Test Song", "body": "royalty data", "userId": 1}  # Create request body
    response = session.post(f"{BASE_URL}/posts", json=payload)  # Make POST request
    data = response.json()  # Parse response JSON
    assert "id" in data  # Assert response contains "id" key
    assert isinstance(data["id"], int)  # Assert "id" value is an integer


def test_create_post_echoes_payload(session):  # Test that POST response includes the sent payload
    payload = {"title": "My Title", "body": "My Body", "userId": 42}  # Create request body
    response = session.post(f"{BASE_URL}/posts", json=payload)  # Make POST request
    data = response.json()  # Parse response JSON
    assert data["title"] == payload["title"]  # Assert title echoed back correctly
    assert data["body"] == payload["body"]  # Assert body echoed back correctly
    assert data["userId"] == payload["userId"]  # Assert userId echoed back correctly


# ─────────────────────────────────────────
# RESPONSE HEADERS
# ─────────────────────────────────────────

def test_response_content_type_is_json(session):  # Test that response has correct Content-Type header
    response = session.get(f"{BASE_URL}/posts/1")  # Make GET request
    assert "application/json" in response.headers["Content-Type"]  # Assert Content-Type header contains "application/json"


# ─────────────────────────────────────────
# HELPER PATTERN: validate schema of every item in a list
# ─────────────────────────────────────────

REQUIRED_POST_KEYS = {"id", "title", "body", "userId"}  # Define required keys in each post object

def test_all_posts_have_required_keys(session):  # Test that every post in list has all required keys
    response = session.get(f"{BASE_URL}/posts")  # Make GET request to fetch all posts
    posts = response.json()  # Parse response as JSON list
    for post in posts:  # Loop through each post
        missing = REQUIRED_POST_KEYS - set(post.keys())  # Find keys that are required but missing
        assert not missing, f"Post {post.get('id')} missing keys: {missing}"  # Assert no missing keys (show error if any)
