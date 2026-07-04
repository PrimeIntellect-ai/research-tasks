# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"
TOKEN = "secret graph dataset"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_unauthorized_access():
    """Test that endpoints return 401 Unauthorized without correct token."""
    url = f"{BASE_URL}/api/hindex?author=Alice"

    # No header
    try:
        resp = requests.get(url, timeout=2)
        assert resp.status_code == 401, f"Expected 401 without auth header, got {resp.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

    # Wrong token
    try:
        resp = requests.get(url, headers={"Authorization": "Bearer wrong token"}, timeout=2)
        assert resp.status_code == 401, f"Expected 401 with wrong auth header, got {resp.status_code}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")

def test_hindex_alice():
    """Test the h-index calculation for Alice."""
    url = f"{BASE_URL}/api/hindex?author=Alice"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

        data = resp.json()
        assert data.get("author") == "Alice", f"Expected author 'Alice', got {data.get('author')}"
        assert data.get("h_index") == 3, f"Expected h_index 3 for Alice, got {data.get('h_index')}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

def test_hindex_bob():
    """Test the h-index calculation for Bob."""
    url = f"{BASE_URL}/api/hindex?author=Bob"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

        data = resp.json()
        assert data.get("author") == "Bob", f"Expected author 'Bob', got {data.get('author')}"
        assert data.get("h_index") == 1, f"Expected h_index 1 for Bob, got {data.get('h_index')}"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

def test_top_papers():
    """Test the top_papers endpoint."""
    url = f"{BASE_URL}/api/top_papers"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"

        data = resp.json()
        assert isinstance(data, list), f"Expected response to be a list, got {type(data)}"
        assert len(data) == 5, f"Expected 5 top papers, got {len(data)}"

        expected_counts = {"Paper A": 5, "Paper F": 5, "Paper B": 4, "Paper C": 3, "Paper D": 3}

        for paper in data:
            title = paper.get("title")
            count = paper.get("citation_count")
            assert title in expected_counts, f"Unexpected paper in top 5: {title}"
            assert expected_counts[title] == count, f"Expected {expected_counts[title]} citations for {title}, got {count}"

    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server: {e}")
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")