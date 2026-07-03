# test_final_state.py

import socket
import requests
import time
import uuid
import pytest

def test_aggregation_service():
    """
    Tests the aggregation service by sending a payload with unique IDs,
    malformed notes, and duplicates, and verifies the metrics endpoint.
    """
    # 1. Attempt to get initial state (in case the service is already running and has state)
    initial_count = 0
    initial_amount = 0.0
    try:
        resp = requests.get("http://127.0.0.1:8002/stats", timeout=2)
        if resp.status_code == 200:
            data = resp.json()
            initial_count = data.get("unique_count", 0)
            initial_amount = data.get("total_amount", 0.0)
    except Exception:
        # Service might be fresh or not responding yet, we'll catch failures later
        pass

    # 2. Generate a unique prefix to avoid collisions with previous test runs
    prefix = str(uuid.uuid4())[:8] + "_"

    # 3. Construct the payload with the exact test cases from the truth
    payload = (
        f"{prefix}tx100,1700000000,10.50,clean note\n"
        f"{prefix}tx101,1700000001,20.00,malformed \\u2028 note\n"
        f"{prefix}tx100,1700000002,500.00,duplicate id should be ignored\n"
        f"{prefix}tx102,1700000003,5.25,another clean note\n"
    )

    # 4. Send the payload via TCP to the ingestion port
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(("127.0.0.1", 8001))
        s.sendall(payload.encode("utf-8"))
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect and send TCP payload to 127.0.0.1:8001. Is the ingestion service running? Error: {e}")

    # Give the service a moment to process the ingested data
    time.sleep(1)

    # 5. Query the HTTP metrics endpoint
    try:
        resp = requests.get("http://127.0.0.1:8002/stats", timeout=3)
        assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}"
        final_data = resp.json()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to get HTTP response from 127.0.0.1:8002/stats. Is the HTTP service running? Error: {e}")
    except ValueError:
        pytest.fail(f"Failed to parse JSON from HTTP response. Raw response: {resp.text}")

    # 6. Validate the response structure and values
    assert "unique_count" in final_data, f"JSON response missing 'unique_count'. Response: {final_data}"
    assert "total_amount" in final_data, f"JSON response missing 'total_amount'. Response: {final_data}"

    final_count = final_data["unique_count"]
    final_amount = final_data["total_amount"]

    expected_count_diff = 3
    expected_amount_diff = 35.75

    actual_count_diff = final_count - initial_count
    actual_amount_diff = final_amount - initial_amount

    assert actual_count_diff == expected_count_diff, \
        f"Expected unique_count to increase by {expected_count_diff} (3 unique valid rows), but it increased by {actual_count_diff}. " \
        f"Initial: {initial_count}, Final: {final_count}. Did the parser drop the row with '\\u'?"

    assert abs(actual_amount_diff - expected_amount_diff) < 0.01, \
        f"Expected total_amount to increase by {expected_amount_diff} (10.50 + 20.00 + 5.25), but it increased by {actual_amount_diff}. " \
        f"Initial: {initial_amount}, Final: {final_amount}. Check deduplication and parsing logic."