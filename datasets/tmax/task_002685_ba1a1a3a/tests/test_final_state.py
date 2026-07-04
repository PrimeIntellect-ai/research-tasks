# test_final_state.py

import os
import json
import urllib.request
import urllib.error

def test_json_output():
    json_path = "/home/user/hourly_region_counts.json"
    assert os.path.exists(json_path), f"JSON file missing at {json_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert isinstance(data, list), "JSON output must be a list of dictionaries."

    expected = [
        {"hour": "2023-10-24 14:00", "ASIA": 1, "EU": 2, "US": 0},
        {"hour": "2023-10-24 15:00", "ASIA": 0, "EU": 1, "US": 1},
        {"hour": "2023-10-24 16:00", "ASIA": 0, "EU": 0, "US": 1}
    ]

    assert len(data) == len(expected), f"Expected {len(expected)} rows, got {len(data)}"

    for d, e in zip(data, expected):
        assert d.get("hour") == e["hour"], f"Expected hour {e['hour']}, got {d.get('hour')}"
        assert int(d.get("ASIA", 0)) == e["ASIA"], f"Expected ASIA count {e['ASIA']} for hour {e['hour']}"
        assert int(d.get("EU", 0)) == e["EU"], f"Expected EU count {e['EU']} for hour {e['hour']}"
        assert int(d.get("US", 0)) == e["US"], f"Expected US count {e['US']} for hour {e['hour']}"

def test_parquet_output():
    parquet_path = "/home/user/hourly_region_counts.parquet"
    assert os.path.exists(parquet_path), f"Parquet file missing at {parquet_path}"

    with open(parquet_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"PAR1", f"File {parquet_path} is not a valid Parquet file (missing PAR1 magic bytes)."

def test_http_server():
    url = "http://localhost:8080/hourly_region_counts.json"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP status 200, got {response.status}"
            content = response.read()
            assert len(content) > 0, "Downloaded file is empty."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to HTTP server on port 8080: {e}"