# test_final_state.py
import os
import requests
import time
import pytest

def wait_for_server(url, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url, timeout=1)
            return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

@pytest.fixture(scope="session", autouse=True)
def ensure_server_running():
    server_up = wait_for_server("http://127.0.0.1:8080/")
    # We don't assert here, we let the individual tests fail if the server is down.

def test_intro_route():
    """Verify the /intro route serves the modified intro.txt."""
    url = "http://127.0.0.1:8080/intro"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for /intro, got {response.status_code}"
    content = response.text
    assert "[INTERNAL DRAFT]" in content[:20], "Response did not start with [INTERNAL DRAFT]"
    assert "Welcome to the v2.0 documentation. This v2.0 system is deprecated." in content, \
        f"Expected modified text in response, got: {content}"

def test_api_route():
    """Verify the /api route serves the modified api.txt."""
    url = "http://127.0.0.1:8080/api"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for /api, got {response.status_code}"
    content = response.text
    assert "[INTERNAL DRAFT]" in content[:20], "Response did not start with [INTERNAL DRAFT]"
    assert "API v2.0 reference guide." in content, \
        f"Expected modified text in response, got: {content}"

def test_architecture_route():
    """Verify the /architecture route serves the OCR output."""
    url = "http://127.0.0.1:8080/architecture"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200 for /architecture, got {response.status_code}"
    content = response.text
    assert "[INTERNAL DRAFT]" in content[:20], "Response did not start with [INTERNAL DRAFT]"
    assert "SYSTEM_ARCHITECTURE_SECRET_8842" in content, \
        f"Expected OCR text in response, got: {content}"

def test_404_route():
    """Verify that an unknown route returns 404."""
    url = "http://127.0.0.1:8080/not_found"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to server at {url}: {e}")

    assert response.status_code == 404, f"Expected status 404 for unknown route, got {response.status_code}"

def test_files_exist_and_modified():
    """Verify that the files exist on disk and were modified correctly."""
    assert os.path.isdir("/app/docs"), "/app/docs directory is missing."

    intro_path = "/app/docs/intro.txt"
    assert os.path.isfile(intro_path), f"{intro_path} is missing."
    with open(intro_path, "r") as f:
        content = f.read()
        assert content.startswith("[INTERNAL DRAFT]\n"), f"{intro_path} does not start with [INTERNAL DRAFT]\\n"
        assert "v2.0" in content and "v1.0" not in content, f"{intro_path} was not updated to v2.0 correctly."

    diagram_path = "/app/docs/diagram.txt"
    assert os.path.isfile(diagram_path), f"{diagram_path} is missing."
    with open(diagram_path, "r") as f:
        content = f.read()
        assert content.startswith("[INTERNAL DRAFT]\n"), f"{diagram_path} does not start with [INTERNAL DRAFT]\\n"
        assert "SYSTEM_ARCHITECTURE_SECRET_8842" in content, f"{diagram_path} does not contain OCR text."