# test_final_state.py

import requests
import pytest

def test_api_response_and_parameters():
    url = "http://127.0.0.1:8080/model"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url} or make a request: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, but got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Response text: {response.text}")

    for key in ["K", "D0", "r"]:
        assert key in data, f"Key '{key}' is missing from the JSON response"

    K = data["K"]
    D0 = data["D0"]
    r = data["r"]

    assert isinstance(K, (int, float)), f"K must be a number, got {type(K)}"
    assert isinstance(D0, (int, float)), f"D0 must be a number, got {type(D0)}"
    assert isinstance(r, (int, float)), f"r must be a number, got {type(r)}"

    assert 0.76 <= K <= 0.84, f"K value {K} is out of expected range [0.76, 0.84]"
    assert 0.04 <= D0 <= 0.06, f"D0 value {D0} is out of expected range [0.04, 0.06]"
    assert 0.13 <= r <= 0.17, f"r value {r} is out of expected range [0.13, 0.17]"