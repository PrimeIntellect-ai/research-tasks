# test_final_state.py
import os
import pytest
import requests

def test_fast_bayes_installed():
    """Verify that fast_bayes is successfully installed and importable."""
    try:
        import fast_bayes
    except ImportError as e:
        pytest.fail(f"Failed to import fast_bayes. The package was not installed correctly. Error: {e}")

def test_best_alpha_file():
    """Verify that the best_alpha.txt file exists and contains a valid alpha value."""
    alpha_file = "/home/user/best_alpha.txt"
    assert os.path.isfile(alpha_file), f"File {alpha_file} does not exist."

    with open(alpha_file, "r") as f:
        content = f.read().strip()

    try:
        alpha_val = float(content)
    except ValueError:
        pytest.fail(f"Content of {alpha_file} is not a valid float: '{content}'")

    assert alpha_val in [0.1, 1.0, 10.0], f"Expected alpha to be one of [0.1, 1.0, 10.0], but got {alpha_val}"

def test_server_unauthorized():
    """Verify that the server rejects requests without the correct Bearer token."""
    url = "http://127.0.0.1:8080/evaluate"
    payload = {"features": [0.5, -1.2, 3.4, 0.1]}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 401, f"Expected 401 Unauthorized for request without token, but got {response.status_code}. Response: {response.text}"

def test_server_authorized():
    """Verify that the server accepts authorized requests and returns the correct JSON schema."""
    url = "http://127.0.0.1:8080/evaluate"
    payload = {"features": [0.5, -1.2, 3.4, 0.1]}
    headers = {"Authorization": "Bearer ds-research-2024"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected 200 OK for authorized request, but got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "quality_score" in data, f"Response JSON missing 'quality_score'. Got: {data}"
    assert "inference_time_ms" in data, f"Response JSON missing 'inference_time_ms'. Got: {data}"

    assert isinstance(data["quality_score"], (int, float)), f"quality_score must be a float, got {type(data['quality_score'])}"
    assert isinstance(data["inference_time_ms"], (int, float)), f"inference_time_ms must be a float, got {type(data['inference_time_ms'])}"

    assert 0.0 <= float(data["quality_score"]) <= 1.0, f"quality_score should be a probability between 0 and 1, got {data['quality_score']}"
    assert float(data["inference_time_ms"]) >= 0.0, f"inference_time_ms should be non-negative, got {data['inference_time_ms']}"