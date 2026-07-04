# test_final_state.py
import sys
import hashlib
import requests
import pytest

def test_semantic_version_fixed():
    """Verify that the vendored semantic_version constraint bug was fixed."""
    vendored_path = "/app/semantic_version"
    if vendored_path not in sys.path:
        sys.path.insert(0, vendored_path)

    try:
        import semantic_version
    except ImportError:
        pytest.fail(f"Could not import semantic_version from {vendored_path}")

    try:
        spec = semantic_version.SimpleSpec(">=1.5.0")
        ver = semantic_version.Version("1.5.0")
        assert spec.match(ver) is True, "The semantic_version bug is not fixed. '>=1.5.0' should match '1.5.0'."
    except Exception as e:
        pytest.fail(f"Error evaluating semantic_version constraints: {e}")

def test_api_resolution_success():
    """Verify the API returns the correct resolved versions and checksum."""
    url = "http://127.0.0.1:8888/resolve"
    params = {"pkg": "frontend", "req": ">=1.0.0"}
    headers = {"Authorization": "Bearer test-agent-token-99"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the resolution API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "resolved" in data, "Missing 'resolved' key in JSON response."
    assert "checksum" in data, "Missing 'checksum' key in JSON response."

    resolved = data["resolved"]
    expected_resolved = {
        "frontend": "1.2.0",
        "backend": "2.2.0",
        "db": "1.0.1"
    }

    for pkg, expected_ver in expected_resolved.items():
        actual_ver = resolved.get(pkg)
        assert actual_ver == expected_ver, f"Expected resolved package '{pkg}' to be '{expected_ver}', got '{actual_ver}'"

    # Compute expected checksum dynamically
    resolved_strings = [f"{k}=={v}" for k, v in expected_resolved.items()]
    resolved_strings.sort()
    joined_str = "\n".join(resolved_strings)
    expected_checksum = hashlib.sha256(joined_str.encode('utf-8')).hexdigest()

    assert data["checksum"] == expected_checksum, f"Checksum mismatch. Expected '{expected_checksum}', got '{data['checksum']}'"

def test_api_unauthorized():
    """Verify the API rejects requests without the correct Authorization header."""
    url = "http://127.0.0.1:8888/resolve"
    params = {"pkg": "frontend", "req": ">=1.0.0"}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the resolution API at {url}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing auth, got {response.status_code}"