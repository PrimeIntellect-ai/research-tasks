# test_final_state.py
import requests
import time

def test_api_response():
    """Test that the API server is running, accepts the correct authorization, and returns valid data."""
    url = "http://127.0.0.1:8888/analysis"
    headers = {"Authorization": "Bearer perf-agent-secret"}

    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=5)
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                raise AssertionError("Could not connect to the API server at http://127.0.0.1:8888. Ensure the server is running.")
            time.sleep(1)

    assert response is not None
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f"Response is not valid JSON: {response.text}")

    assert "wasserstein" in data, "Missing 'wasserstein' key in JSON response"
    assert "posterior_mean" in data, "Missing 'posterior_mean' key in JSON response"
    assert "posterior_std" in data, "Missing 'posterior_std' key in JSON response"

    wasserstein = data["wasserstein"]
    posterior_mean = data["posterior_mean"]
    posterior_std = data["posterior_std"]

    assert isinstance(wasserstein, (int, float)), f"wasserstein must be a number, got {type(wasserstein)}"
    assert isinstance(posterior_mean, (int, float)), f"posterior_mean must be a number, got {type(posterior_mean)}"
    assert isinstance(posterior_std, (int, float)), f"posterior_std must be a number, got {type(posterior_std)}"

    assert 48.5 <= wasserstein <= 49.5, f"wasserstein value {wasserstein} is out of expected range [48.5, 49.5]"
    assert 288.0 <= posterior_mean <= 290.0, f"posterior_mean value {posterior_mean} is out of expected range [288.0, 290.0]"
    assert 26.0 <= posterior_std <= 31.0, f"posterior_std value {posterior_std} is out of expected range [26.0, 31.0]"

def test_api_unauthorized():
    """Test that the API server does not return the secret data when unauthorized."""
    url = "http://127.0.0.1:8888/analysis"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            try:
                data = response.json()
                if "wasserstein" in data:
                    raise AssertionError("API returned the analysis data without the required Authorization header.")
            except ValueError:
                pass
    except requests.exceptions.ConnectionError:
        pass # Server might be down, but that's handled by the primary test.