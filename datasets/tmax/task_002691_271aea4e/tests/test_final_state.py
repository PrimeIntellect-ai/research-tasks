# test_final_state.py

import pytest
import requests

def test_unauthorized_missing_header():
    """Test that requests without the Authorization header return 401."""
    url = "http://127.0.0.1:8000/process"
    data = "id,text_a,text_b\n1,a,a\n"
    try:
        response = requests.post(url, data=data, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the Nginx reverse proxy: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for missing auth, got {response.status_code}"

def test_unauthorized_invalid_header():
    """Test that requests with an invalid Authorization header return 401."""
    url = "http://127.0.0.1:8000/process"
    headers = {"Authorization": "Bearer wrong-token"}
    data = "id,text_a,text_b\n1,a,a\n"
    try:
        response = requests.post(url, headers=headers, data=data, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the Nginx reverse proxy: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 for invalid auth, got {response.status_code}"

def test_successful_processing_with_newlines():
    """Test that valid requests return the correctly processed CSV data, including embedded newlines."""
    url = "http://127.0.0.1:8000/process"
    headers = {"Authorization": "Bearer data-science-token"}
    data = (
        "id,text_a,text_b\n"
        '1,"clean","clear"\n'
        '2,"line\nbreak","line\nbreak"\n'
        '3,"kitten","sitting"\n'
    )

    try:
        response = requests.post(url, headers=headers, data=data, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the Nginx reverse proxy: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    expected_output = (
        "[ID: 1] Distance: 2\n"
        "[ID: 2] Distance: 0\n"
        "[ID: 3] Distance: 3\n"
    )

    assert response.text == expected_output, f"Response body did not match expected output.\nExpected:\n{expected_output}\nGot:\n{response.text}"