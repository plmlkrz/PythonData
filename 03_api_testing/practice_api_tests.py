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
import responses

BASE_URL = "https://jsonplaceholder.typicode.com"

# Fixtures

@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    yield s
    s.close()

def mock_post(post_id, user_id=1):
    return {
        "id": post_id,
        "title": f"Post {post_id} Title",
        "body": f"Post {post_id} Body",
        "userId": user_id
    }

def setup_mock_posts():
    posts = [mock_post(i, (i % 10) + 1) for i in range(1, 101)]
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts",
        json=posts,
        status=200,
        headers={"Content-Type": "application/json"}
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/1",
        json=mock_post(1),
        status=200,
        headers={"Content-Type": "application/json"}
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/post/1",
        json=mock_post(1),
        status=200,
        headers={"Content-Type": "application/json"}
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/post/999999",
        status=404
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/posts",
        status=201,
        headers={"Content-Type": "application/json"}
    )

# GET

@responses.activate
def test_get_post_returns_200(session):
    responses.add(responses.GET, f"{BASE_URL}/post/1", json=mock_post(1), status=200)
    response = session.get(f"{BASE_URL}/post/1")
    assert response.status_code == 200

@responses.activate
def test_get_post_json_structure(session):
    responses.add(responses.GET, f"{BASE_URL}/post/1", json=mock_post(1), status=200)
    response = session.get(f"{BASE_URL}/post/1")
    data = response.json()
    assert "id" in data
    assert "title" in data
    assert "body" in data
    assert "userId" in data

@responses.activate
def test_get_post_correct_id(session):
    responses.add(responses.GET, f"{BASE_URL}/post/1", json=mock_post(1), status=200)
    response = session.get(f"{BASE_URL}/post/1")
    data = response.json()
    assert data["id"] == 1

@responses.activate
def test_get_nonexistent_post_returns_404(session):
    responses.add(responses.GET, f"{BASE_URL}/post/999999", status=404)
    response = session.get(f"{BASE_URL}/post/999999")
    assert response.status_code == 404

# Get - read a collection

@responses.activate
def test_get_all_post_returns_list(session):
    posts = [mock_post(i) for i in range(1, 101)]
    responses.add(responses.GET, f"{BASE_URL}/post", json=posts, status=200)
    response = session.get(f"{BASE_URL}/post")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100

@responses.activate
def test_get_post_by_user(session):
    posts = [mock_post(i, 1) for i in range(1, 11)]
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts",
        json=posts,
        status=200,
        match=[responses.matchers.query_param_matcher({"userId": "1"})]
    )
    response = session.get(f"{BASE_URL}/posts", params={"userId": 1})
    data = response.json()
    assert all(post["userId"] == 1 for post in data)


# POST - Create a resource

@responses.activate
def test_create_post_returns_201(session):
    def request_callback(request):
        return (201, {}, '{"id": 101, "title": "Test Song", "body": "royalty data", "userId": 1}')
    responses.add_callback(
        responses.POST,
        f"{BASE_URL}/posts",
        callback=request_callback,
        content_type="application/json"
    )
    payload = {"title" : "Test Song", "body" : "royalty data", "userId": 1}
    response = session.post(f"{BASE_URL}/posts", json=payload)
    assert response.status_code == 201

@responses.activate
def test_create_post_response_contains_id(session):
    def request_callback(request):
        return (201, {}, '{"id": 101, "title": "Test Song", "body": "royalty data", "userId": 1}')
    responses.add_callback(
        responses.POST,
        f"{BASE_URL}/posts",
        callback=request_callback,
        content_type="application/json"
    )
    payload = {"title" : "Test Song", "body" : "royalty data", "userId": 1}
    response = session.post(f"{BASE_URL}/posts", json=payload)
    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)

@responses.activate
def test_create_post_echoes_payload(session):
    def request_callback(request):
        import json
        payload = json.loads(request.body)
        response_data = {**payload, "id": 101}
        return (201, {}, json.dumps(response_data))
    responses.add_callback(
        responses.POST,
        f"{BASE_URL}/posts",
        callback=request_callback,
        content_type="application/json"
    )
    payload = {"title" : "Test Song", "body": "My Body", "userId" : 42 }
    response = session.post(f"{BASE_URL}/posts", json=payload)
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]

# Response Headers

@responses.activate
def test_response_content_type_json(session):
    responses.add(
        responses.GET,
        f"{BASE_URL}/posts/1",
        json=mock_post(1),
        status=200,
        headers={"Content-Type": "application/json"}
    )
    response = session.get(f"{BASE_URL}/posts/1")
    assert "application/json" in response.headers["Content-Type"]

#Helper Pattern

REQUIRED_POST_KEYS = {"id", "title", "body", "userId"}
@responses.activate
def test_all_posts_have_required_keys(session):
    posts = [mock_post(i) for i in range(1, 101)]
    responses.add(responses.GET, f"{BASE_URL}/posts", json=posts, status=200)
    response = session.get(f"{BASE_URL}/posts")
    posts = response.json()
    for post in posts:
        missing = REQUIRED_POST_KEYS - set(post.keys())
        assert not missing, f"post {post.get("id")} missing keys: {missing}"


