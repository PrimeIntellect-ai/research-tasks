# test_final_state.py
import requests

def test_http_server_artifacts():
    url = "http://127.0.0.1:8080/artifacts"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to the server at {url}: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    expected_artifacts = [
        {"id": "1", "name": "sys-core.tar.gz", "size": 450},
        {"id": "3", "name": "net-utils.tgz", "size": 890},
        {"id": "5", "name": "auth-lib.tar.gz", "size": 120}
    ]

    assert "artifacts" in data, "JSON response missing 'artifacts' key"
    assert data["artifacts"] == expected_artifacts, f"Expected artifacts {expected_artifacts}, got {data['artifacts']}"