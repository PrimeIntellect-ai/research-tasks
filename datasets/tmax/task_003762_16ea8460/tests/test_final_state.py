# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080/api/v1/anomalies"

def fetch_anomalies(machine_id: str):
    try:
        response = requests.get(f"{BASE_URL}?id={machine_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server or bad response for machine {machine_id}: {e}")
    except ValueError as e:
        pytest.fail(f"Response for machine {machine_id} is not valid JSON: {e}")

def test_a73b_records():
    """Verify that records for A73B are correctly filtered, deduplicated, and formatted."""
    data = fetch_anomalies("A73B")

    assert isinstance(data, list), "Response must be a JSON array"
    assert len(data) == 1, f"Expected exactly 1 record for A73B (after deduplication and filtering), got {len(data)}"

    record = data[0]
    assert record.get("timestamp") == "2023-10-01T10:00:00Z"
    assert record.get("machine_id") == "A73B"
    assert float(record.get("temperature")) == 45.2
    assert str(record.get("sensor_reading")) == "100"
    assert record.get("status_notes") == "Normal operation"

def test_d90e_records():
    """Verify that records for D90E are correctly decoded to UTF-8 and formatted."""
    data = fetch_anomalies("D90E")

    assert isinstance(data, list), "Response must be a JSON array"
    assert len(data) == 1, f"Expected exactly 1 record for D90E, got {len(data)}"

    record = data[0]
    assert record.get("timestamp") == "2023-10-01T10:10:00Z"
    assert record.get("machine_id") == "D90E"
    assert float(record.get("temperature")) == 10.5
    assert str(record.get("sensor_reading")) == "50"
    assert record.get("status_notes") == "System offline due to résumé", "Encoding issue: status_notes not properly converted to UTF-8"

def test_o22x_records():
    """Verify that records for O22X are correctly formatted."""
    data = fetch_anomalies("O22X")

    assert isinstance(data, list), "Response must be a JSON array"
    assert len(data) == 1, f"Expected exactly 1 record for O22X, got {len(data)}"

    record = data[0]
    assert record.get("timestamp") == "2023-10-01T10:15:00Z"
    assert record.get("machine_id") == "O22X"
    assert float(record.get("temperature")) == -10.0
    assert str(record.get("sensor_reading")) == "10"
    assert record.get("status_notes") == "Cold start"