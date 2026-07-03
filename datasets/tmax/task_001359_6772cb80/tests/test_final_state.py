# test_final_state.py

import urllib.request
import json
import pytest

def test_pipeline_accuracy():
    url = "http://localhost:5002/api/v1/stats"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Failed to fetch stats from Data Warehouse API at {url}: {e}")

    assert "accuracy" in data, "Response from Data Warehouse API is missing the 'accuracy' key."
    accuracy = data["accuracy"]
    threshold = 0.95

    assert accuracy >= threshold, f"Pipeline accuracy {accuracy} is below the required threshold of {threshold}."