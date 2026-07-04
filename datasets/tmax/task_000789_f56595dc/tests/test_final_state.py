# test_final_state.py

import requests
import pytest

def test_server_response():
    """Test that the server on 127.0.0.1:9000 returns the correct transition counts."""
    url = "http://127.0.0.1:9000/"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"

    expected_body = "AA:0,AC:2,AG:0,AT:0,CA:0,CC:0,CG:0,CT:2,GA:1,GC:0,GG:0,GT:0,TA:1,TC:0,TG:1,TT:0"
    actual_body = response.text.strip()

    assert actual_body == expected_body, (
        f"Incorrect response body.\n"
        f"Expected: {expected_body}\n"
        f"Actual:   {actual_body}"
    )