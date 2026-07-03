# test_final_state.py
import requests
import math
import pytest
import time

def wait_for_service(url, timeout=5):
    """Wait for the service to become available."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False

def test_nginx_proxy_and_backend_response():
    url = "http://127.0.0.1:8080/embed?id=1"

    # Wait briefly for services to be up in case they were just started
    wait_for_service(url)

    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Make sure Nginx is proxying to the C backend."

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "id" in data, "Response JSON missing 'id' field"
    assert "embedding" in data, "Response JSON missing 'embedding' field"

    embedding = data["embedding"]
    assert isinstance(embedding, list), "'embedding' should be a list"
    assert len(embedding) > 0, "'embedding' list is empty"

    # Check L2 norm
    sq_sum = sum(x * x for x in embedding)
    norm = math.sqrt(sq_sum)

    assert math.isclose(norm, 1.0, rel_tol=1e-3, abs_tol=1e-3), f"L2 norm of embedding is {norm}, expected ~1.0. Mathematical bug in C code might not be fixed."

    # Check that it's not all zeros or truncated
    assert any(x != 0.0 for x in embedding), "Embedding values are all zero, precision bug not fixed"
    assert any(not float(x).is_integer() for x in embedding), "Embedding values appear to be truncated to integers, precision bug not fixed"

def test_multiple_ids():
    for test_id in [5, 10, 42]:
        url = f"http://127.0.0.1:8080/embed?id={test_id}"
        try:
            response = requests.get(url, timeout=2)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to Nginx for id {test_id}: {e}")

        assert response.status_code == 200, f"Expected HTTP 200 for id {test_id}, got {response.status_code}"
        data = response.json()
        embedding = data.get("embedding", [])

        sq_sum = sum(x * x for x in embedding)
        norm = math.sqrt(sq_sum)
        assert math.isclose(norm, 1.0, rel_tol=1e-3, abs_tol=1e-3), f"L2 norm of embedding for id {test_id} is {norm}, expected ~1.0"