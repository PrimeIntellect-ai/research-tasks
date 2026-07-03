# test_final_state.py

import pytest
import requests
import time

def test_daemon_fixed_and_running():
    """
    Test that the daemon is running on 127.0.0.1:8080, accepts metrics,
    and no longer exhibits the backdoor behavior when the X-Internal-Debug header is present.
    """
    base_url = "http://127.0.0.1:8080"

    # Wait briefly in case the server is just starting up
    time.sleep(1)

    try:
        # Get initial stats in case the agent left the server running with prior data
        resp_initial = requests.get(f"{base_url}/stats", timeout=2)
        assert resp_initial.status_code == 200, f"Failed to get initial stats, status: {resp_initial.status_code}"

        initial_data = resp_initial.json()
        assert "average" in initial_data, "Response missing 'average' key"
        assert "count" in initial_data, "Response missing 'count' key"

        initial_count = initial_data["count"]
        initial_average = initial_data["average"]
        initial_sum = initial_count * initial_average

        # Submit first value
        resp_post1 = requests.post(f"{base_url}/submit?value=10", timeout=2)
        assert resp_post1.status_code == 200, f"First POST failed, status: {resp_post1.status_code}"

        # Submit second value with the malicious header
        headers = {"X-Internal-Debug": "admin"}
        resp_post2 = requests.post(f"{base_url}/submit?value=5", headers=headers, timeout=2)
        assert resp_post2.status_code == 200, f"Second POST failed, status: {resp_post2.status_code}"

        # Get final stats
        resp_final = requests.get(f"{base_url}/stats", timeout=2)
        assert resp_final.status_code == 200, f"Failed to get final stats, status: {resp_final.status_code}"

        final_data = resp_final.json()
        final_count = final_data["count"]
        final_average = final_data["average"]

        expected_count = initial_count + 2
        expected_sum = initial_sum + 10 + 5
        expected_average = expected_sum / expected_count

        assert final_count == expected_count, f"Expected count {expected_count}, got {final_count}"

        # If the backdoor is still present, the 5 would be squared to 25, adding 35 total instead of 15.
        # We check if the average matches the expected (non-squared) average.
        # Use a small tolerance for floating point comparisons.
        assert abs(final_average - expected_average) < 1e-5, \
            f"Expected average {expected_average}, got {final_average}. The backdoor might still be active."

    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the daemon at 127.0.0.1:8080. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail("Requests to the daemon timed out.")
    except ValueError:
        pytest.fail("Daemon did not return valid JSON.")