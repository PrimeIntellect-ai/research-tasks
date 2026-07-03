# test_final_state.py

import pytest
import requests
import time

def test_etl_server_response():
    url = "http://127.0.0.1:8080/"

    # Retry a few times in case the server is slightly delayed in starting or responding
    max_retries = 5
    response = None
    last_exception = None

    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=3)
            break
        except requests.exceptions.RequestException as e:
            last_exception = e
            time.sleep(1)

    if response is None:
        pytest.fail(f"Failed to connect to the ETL server at {url}. Last error: {last_exception}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "global_max" in data, "JSON payload missing 'global_max' key"
    assert "transcript" in data, "JSON payload missing 'transcript' key"

    # Verify global max
    try:
        global_max = float(data["global_max"])
    except ValueError:
        pytest.fail(f"global_max is not a valid number: {data['global_max']}")

    assert global_max == 22.4, f"Expected global_max to be 22.4, got {global_max}"

    # Verify transcript normalization
    transcript = data["transcript"]

    # Check for transliterated words
    assert "Motorhead" in transcript, f"Expected 'Motorhead' in transcript, got: {transcript}"
    assert "resume" in transcript, f"Expected 'resume' in transcript, got: {transcript}"
    assert "cafe" in transcript, f"Expected 'cafe' in transcript, got: {transcript}"

    # Check that original non-ASCII characters are removed or replaced
    assert "ö" not in transcript, "Found 'ö' in transcript, it should have been normalized to ASCII"
    assert "é" not in transcript, "Found 'é' in transcript, it should have been normalized to ASCII"

    # Strictly ensure the transcript is valid ASCII
    try:
        transcript.encode('ascii')
    except UnicodeEncodeError:
        pytest.fail(f"Transcript contains non-ASCII characters despite normalization requirement: {transcript}")