# test_final_state.py

import time
import requests
import pytest

def test_end_to_end_pipeline():
    base_url = "http://127.0.0.1:8080"

    # 1. Send CSV payload
    csv_payload = {
        "format": "csv", 
        "data": "id,timestamp,review_text\n1,1672531200,\"This is a great product,\nI really loved it!\"\n2,12/31/2022 15:30,\"Terrible.\""
    }
    try:
        res_csv = requests.post(f"{base_url}/ingest", json=csv_payload, timeout=5)
        assert res_csv.status_code == 200, f"Failed to post CSV payload, status code: {res_csv.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or ingestion service: {e}")

    # 2. Send JSON payload
    json_payload = {
        "format": "json", 
        "data": "[{\"id\":\"3\",\"timestamp\":\"1672617600\",\"review_text\":\"Okay product\"}]"
    }
    try:
        res_json = requests.post(f"{base_url}/ingest", json=json_payload, timeout=5)
        assert res_json.status_code == 200, f"Failed to post JSON payload, status code: {res_json.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080 or ingestion service: {e}")

    # 3. Wait for worker to process
    time.sleep(3)

    # 4. Query ID 1
    try:
        res_q1 = requests.get(f"{base_url}/query?id=1", timeout=5)
        assert res_q1.status_code == 200, f"Query for ID 1 failed with status code: {res_q1.status_code}"
        data_q1 = res_q1.json()
        assert data_q1.get("id") == "1", f"Expected id '1', got {data_q1.get('id')}"
        assert data_q1.get("timestamp") == "2023-01-01 00:00:00", f"Expected timestamp '2023-01-01 00:00:00', got {data_q1.get('timestamp')}"
        assert data_q1.get("review_text") == "This is a great product,\nI really loved it!", f"Expected specific review text with newline, got {data_q1.get('review_text')}"
        assert data_q1.get("word_count") == 9, f"Expected word_count 9, got {data_q1.get('word_count')}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to query ID 1: {e}")
    except ValueError:
        pytest.fail(f"Response for ID 1 was not valid JSON: {res_q1.text}")

    # 5. Query ID 2
    try:
        res_q2 = requests.get(f"{base_url}/query?id=2", timeout=5)
        assert res_q2.status_code == 200, f"Query for ID 2 failed with status code: {res_q2.status_code}"
        data_q2 = res_q2.json()
        assert data_q2.get("id") == "2", f"Expected id '2', got {data_q2.get('id')}"
        assert data_q2.get("timestamp") == "2022-12-31 15:30:00", f"Expected timestamp '2022-12-31 15:30:00', got {data_q2.get('timestamp')}"
        assert data_q2.get("review_text") == "Terrible.", f"Expected review text 'Terrible.', got {data_q2.get('review_text')}"
        assert data_q2.get("word_count") == 1, f"Expected word_count 1, got {data_q2.get('word_count')}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to query ID 2: {e}")
    except ValueError:
        pytest.fail(f"Response for ID 2 was not valid JSON: {res_q2.text}")

    # 6. Query ID 3
    try:
        res_q3 = requests.get(f"{base_url}/query?id=3", timeout=5)
        assert res_q3.status_code == 200, f"Query for ID 3 failed with status code: {res_q3.status_code}"
        data_q3 = res_q3.json()
        assert data_q3.get("id") == "3", f"Expected id '3', got {data_q3.get('id')}"
        assert data_q3.get("timestamp") == "2023-01-02 00:00:00", f"Expected timestamp '2023-01-02 00:00:00', got {data_q3.get('timestamp')}"
        assert data_q3.get("review_text") == "Okay product", f"Expected review text 'Okay product', got {data_q3.get('review_text')}"
        assert data_q3.get("word_count") == 2, f"Expected word_count 2, got {data_q3.get('word_count')}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to query ID 3: {e}")
    except ValueError:
        pytest.fail(f"Response for ID 3 was not valid JSON: {res_q3.text}")