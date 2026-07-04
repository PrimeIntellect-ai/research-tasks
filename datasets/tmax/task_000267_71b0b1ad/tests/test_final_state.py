# test_final_state.py
import os
import requests
import pytest

def test_buggy_commit_hash():
    expected_file = "/app/.expected_buggy_commit"
    student_file = "/app/buggy_commit.txt"

    assert os.path.exists(student_file), f"File {student_file} does not exist. Did you write the buggy commit hash?"

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(student_file, "r") as f:
        student_hash = f.read().strip()

    assert student_hash == expected_hash, f"Expected commit hash {expected_hash}, but got {student_hash}."

def test_server_response():
    url = "http://127.0.0.1:8080/"
    headers = {
        "X-Debug-Trace": "true",
        "Authorization": "Bearer secret-agent-123"
    }

    try:
        response = requests.get(url, headers=headers, timeout=3)
    except requests.exceptions.Timeout:
        pytest.fail("Request to server timed out after 3 seconds. The infinite loop might not be fixed.")
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server at 127.0.0.1:8080. Is it running in the background?")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred while connecting to the server: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}."
    assert response.text == "OK", f"Expected response body 'OK', but got '{response.text}'."