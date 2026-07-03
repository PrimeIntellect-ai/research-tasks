# test_final_state.py

import os
import time
import requests
import pytest

def test_executable_exists():
    """Check if the compiled etl_server executable exists."""
    assert os.path.isfile('/app/etl-worker/etl_server'), "The executable '/app/etl-worker/etl_server' was not found. Did you compile the project?"

def test_etl_service_extraction():
    """Send a raw text payload to the ETL service and verify the extracted transaction IDs."""
    url = "http://127.0.0.1:8080/extract"

    payload = (
        "Error log start\n"
        "Details:\n"
        "TXN-ABCD-12345\n"
        "More text\n"
        "Another one: TXN-WXYZ-98765 \n"
        "Invalid ones: TXN-ABC-12345 TXN-ABCDE-12345 TXN-ABCD-1234\n"
        "TXN-ZZZZ-00000\n"
        "End of log."
    )

    expected_ids = ["TXN-ABCD-12345", "TXN-WXYZ-98765", "TXN-ZZZZ-00000"]

    # Retry a few times in case the service takes a moment to be fully responsive
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=payload, timeout=2)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    else:
        pytest.fail(f"Could not connect to the service at {url} after {max_retries} attempts. Is it running on 127.0.0.1:8080?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        result = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(result, list), "Expected the response to be a JSON array."

    # Sort both lists to ensure order doesn't cause a failure if the parallel processing changes it
    assert sorted(result) == sorted(expected_ids), f"Extracted IDs do not match expected. Got: {result}, Expected: {expected_ids}"