# test_final_state.py

import os
import time
import requests
import pytest

API_URL = "http://127.0.0.1:8000/search"

@pytest.fixture(scope="module", autouse=True)
def wait_for_api():
    """Wait for the API to become available."""
    timeout = 10
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Just checking if the port is open and responding to HTTP
            requests.get("http://127.0.0.1:8000/")
            return
        except requests.exceptions.ConnectionError:
            try:
                requests.get(API_URL + "?q=test&limit=1")
                return
            except requests.exceptions.ConnectionError:
                pass
        time.sleep(0.5)
    pytest.fail("API service did not become available on 127.0.0.1:8000 within 10 seconds.")

def test_search_visual_image_object():
    query = "visual image object"
    response = requests.get(API_URL, params={"q": query, "limit": 2})

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "results" in data, "Response JSON must contain a 'results' key."
    results = data["results"]

    assert len(results) <= 2, f"Expected at most 2 results, got {len(results)}."
    assert len(results) > 0, "Expected at least 1 result."

    # Check that the results have the expected keys
    for res in results:
        assert "id" in res, "Result missing 'id' field."
        assert "name" in res, "Result missing 'name' field."
        assert "final_score" in res, "Result missing 'final_score' field."
        assert isinstance(res["final_score"], (int, float)), "final_score must be a number."

    # ImageNet (id=1) should be highly ranked for this query
    ids = [res["id"] for res in results]
    assert 1 in ids, f"Expected ImageNet (id=1) to be in the top 2 results for query '{query}', but got ids {ids}."

def test_search_machine_learning_survival():
    query = "machine learning predicting survival"
    response = requests.get(API_URL, params={"q": query, "limit": 1})

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "results" in data, "Response JSON must contain a 'results' key."
    results = data["results"]

    assert len(results) == 1, f"Expected exactly 1 result, got {len(results)}."

    # Titanic (id=2) should be the top result for this query
    assert results[0]["id"] == 2, f"Expected Titanic (id=2) to be the top result for query '{query}', but got id {results[0]['id']}."

def test_search_logs():
    log_path = "/home/user/search_logs.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "visual image object" in content, "Log file does not contain the first query string."
    assert "machine learning predicting survival" in content, "Log file does not contain the second query string."