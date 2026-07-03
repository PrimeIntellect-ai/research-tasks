# test_final_state.py
import os
import json
import urllib.request
import urllib.error

def test_processed_logs_exist_and_format():
    filepath = "/home/user/processed_logs.jsonl"
    assert os.path.isfile(filepath), f"The file {filepath} does not exist."

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 5, f"Expected 5 lines in {filepath}, but found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in {filepath} is not valid JSON."

        expected_keys = {"timestamp", "lat", "lon", "temperature"}
        assert set(data.keys()) == expected_keys, f"Line {i+1} has incorrect keys. Expected {expected_keys}, got {set(data.keys())}."

        assert isinstance(data["timestamp"], int), f"Line {i+1} timestamp is not an int."
        assert isinstance(data["lat"], float), f"Line {i+1} lat is not a float."
        assert isinstance(data["lon"], float), f"Line {i+1} lon is not a float."
        assert isinstance(data["temperature"], float), f"Line {i+1} temperature is not a float."

def test_processed_logs_data():
    filepath = "/home/user/processed_logs.jsonl"
    assert os.path.isfile(filepath), f"The file {filepath} does not exist."

    with open(filepath, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    assert len(records) == 5, "Expected 5 records."

    # Check interpolated temperatures
    # Row 2 (index 1) should be interpolated to 21.0
    assert abs(records[1]["temperature"] - 21.0) < 0.01, f"Expected temperature 21.0 at row 2, got {records[1]['temperature']}."

    # Row 4 (index 3) should be interpolated to 23.5
    assert abs(records[3]["temperature"] - 23.5) < 0.01, f"Expected temperature 23.5 at row 4, got {records[3]['temperature']}."

def test_summary_json():
    filepath = "/home/user/server_root/summary.json"
    assert os.path.isfile(filepath), f"The file {filepath} does not exist."

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {filepath} is not valid JSON."

    assert "final_row_count" in data, "Key 'final_row_count' missing in summary.json."
    assert data["final_row_count"] == 5, f"Expected final_row_count to be 5, got {data['final_row_count']}."

    assert "total_valid_distance_km" in data, "Key 'total_valid_distance_km' missing in summary.json."
    distance = data["total_valid_distance_km"]
    assert isinstance(distance, (int, float)), "total_valid_distance_km must be a number."
    assert 0.55 <= distance <= 0.57, f"Expected total_valid_distance_km to be between 0.55 and 0.57, got {distance}."

def test_server_running():
    url = "http://127.0.0.1:8080/summary.json"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            content = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to the server at {url}. Is it running? Error: {e}"

    assert status == 200, f"Expected HTTP status 200, got {status}."

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        assert False, f"The response from {url} is not valid JSON."

    assert "final_row_count" in data, "Key 'final_row_count' missing in server response."
    assert data["final_row_count"] == 5, "Server response has incorrect final_row_count."