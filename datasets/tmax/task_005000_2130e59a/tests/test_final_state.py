# test_final_state.py

import os
import time
import requests
import pytest

def test_document_transformation_and_serving():
    src_file = "/home/user/docs/src/draft_release_notes.md"
    expected_endpoint = "http://127.0.0.1:8080/pub_release_notes.html"

    # Write the test file to trigger the watcher
    content = "Release %%STATUS%% on %%DATE%%"
    with open(src_file, "w") as f:
        f.write(content)

    # Wait for the watcher to detect and transformer to process
    time.sleep(3)

    # Make HTTP request to the server
    try:
        response = requests.get(expected_endpoint, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server on 127.0.0.1:8080. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. File might not have been processed or renamed correctly."

    actual_content = response.text.strip()
    expected_content = "Release PUBLISHED on 2024"

    assert actual_content == expected_content, f"Content mismatch. Expected '{expected_content}', but got '{actual_content}'."