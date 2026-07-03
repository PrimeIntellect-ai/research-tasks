# test_final_state.py
import time
import requests
import pytest

def test_log_aggregator_latency_and_correctness():
    """
    Test that the log aggregator returns at least 100,000 sorted logs
    within 0.5 seconds.
    """
    start = time.time()
    try:
        r = requests.get("http://127.0.0.1:5000/logs", timeout=5.0)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to fetch logs from API: {e}")
    except ValueError as e:
        pytest.fail(f"Failed to parse JSON response: {e}")

    latency = time.time() - start

    assert len(data) >= 100000, f"Error: Only received {len(data)} logs. Expected at least 100000."

    # Verify chronological order
    for i in range(1, len(data)):
        if data[i]['timestamp'] < data[i-1]['timestamp']:
            pytest.fail(f"Error: Logs are not strictly sorted at index {i}.")

    assert latency <= 0.5, f"Latency {latency:.4f}s exceeded threshold of 0.5s"