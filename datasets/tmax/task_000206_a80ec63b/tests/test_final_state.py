# test_final_state.py
import requests
import time
import pytest

def test_server_running_and_fast():
    url = "http://127.0.0.1:8080/shortest_path?src=1&dst=50"

    start_time = time.time()
    try:
        response = requests.get(url, timeout=2.0)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")

    duration = time.time() - start_time

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Server did not return valid JSON.")

    assert "path" in data, "JSON response missing 'path' key."
    path = data["path"]

    assert isinstance(path, list), "'path' must be a list."
    assert len(path) >= 2, "Path must contain at least the source and destination."
    assert path[0] == "1", f"Expected path to start with '1', but got {path[0]}"
    assert path[-1] == "50", f"Expected path to end with '50', but got {path[-1]}"

    assert duration < 2.0, f"Request took too long ({duration:.2f}s). The missing index or cross join bug might not be fixed."

def test_engine_code_fixed():
    with open("/app/simple_graph/engine.py", "r") as f:
        content = f.read()

    # Check if index creation is present
    assert "CREATE INDEX" in content.upper(), "Missing index creation in engine.py"

    # Check if the cross join is removed
    assert "FROM edges e, nodes n" not in content, "Implicit cross join still present in engine.py"