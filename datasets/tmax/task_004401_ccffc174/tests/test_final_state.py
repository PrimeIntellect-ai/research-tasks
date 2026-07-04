# test_final_state.py
import requests
import pytest
import concurrent.futures

URL = "http://127.0.0.1:9000/prime_factors"
AUTH_HEADER = {"Authorization": "Bearer 84295"}
PAYLOAD = {"number": 315}
EXPECTED_FACTORS = [3, 3, 5, 7]

def test_server_running_and_auth_required():
    """Verify the server is running and requires authorization."""
    try:
        # Request without auth
        response = requests.post(URL, json=PAYLOAD, timeout=2)
        assert response.status_code in (401, 403), (
            f"Expected 401 or 403 when missing auth, got {response.status_code}"
        )
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {URL}: {e}")

def test_correct_prime_factors():
    """Verify the endpoint returns correct prime factors for a given number."""
    try:
        response = requests.post(URL, headers=AUTH_HEADER, json=PAYLOAD, timeout=2)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        data = response.json()
        assert "factors" in data, "Response JSON missing 'factors' key"

        factors = sorted(data["factors"])
        assert factors == EXPECTED_FACTORS, f"Expected factors {EXPECTED_FACTORS}, got {factors}"
    except requests.RequestException as e:
        pytest.fail(f"Request failed: {e}")
    except ValueError:
        pytest.fail(f"Failed to parse JSON response: {response.text}")

def test_concurrency_no_data_race():
    """Verify that concurrent requests return correct results without data races."""
    def make_request():
        resp = requests.post(URL, headers=AUTH_HEADER, json={"number": 315}, timeout=5)
        if resp.status_code != 200:
            return False, f"Status code {resp.status_code}"
        try:
            data = resp.json()
            if sorted(data.get("factors", [])) != EXPECTED_FACTORS:
                return False, f"Incorrect factors: {data}"
            return True, ""
        except ValueError:
            return False, "Invalid JSON"

    num_requests = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request) for _ in range(num_requests)]

        for future in concurrent.futures.as_completed(futures):
            success, msg = future.result()
            assert success, f"Concurrency test failed: {msg}"