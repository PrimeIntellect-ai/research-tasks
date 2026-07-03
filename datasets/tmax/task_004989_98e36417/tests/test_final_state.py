# test_final_state.py

import json
import subprocess
import time
import requests
import pytest

def get_ground_truth():
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_packets",
        "-of", "json",
        "/app/data_video.mp4"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    packets = data.get("packets", [])
    total_processed = len(packets)

    seen = set()
    deduped = []

    for p in packets:
        size = int(p.get("size", 0))
        flags = p.get("flags", "")
        pts_time = p.get("pts_time", "")

        key = (size, flags)
        if key not in seen:
            seen.add(key)
            deduped.append({"size": size, "pts_time": pts_time})

    total_deduplicated = len(deduped)

    anomalies = []
    for i in range(1, len(deduped)):
        prev_size = deduped[i-1]["size"]
        curr_size = deduped[i]["size"]
        if curr_size > 3 * prev_size:
            anomalies.append(deduped[i]["pts_time"])

    total_anomalies = len(anomalies)

    return {
        "total_processed": total_processed,
        "total_deduplicated": total_deduplicated,
        "total_anomalies": total_anomalies,
        "anomalies": anomalies
    }

@pytest.fixture(scope="module")
def wait_for_service():
    url = "http://127.0.0.1:8080/api/stats"
    max_retries = 30
    for _ in range(max_retries):
        try:
            resp = requests.get(url, timeout=1)
            if resp.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    pytest.fail("Service at 127.0.0.1:8080 did not become ready in time.")

def test_api_stats(wait_for_service):
    truth = get_ground_truth()

    resp = requests.get("http://127.0.0.1:8080/api/stats", timeout=5)
    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response from /api/stats is not valid JSON")

    assert "total_processed" in data, "Missing total_processed in /api/stats"
    assert "total_deduplicated" in data, "Missing total_deduplicated in /api/stats"
    assert "total_anomalies" in data, "Missing total_anomalies in /api/stats"

    assert data["total_processed"] == truth["total_processed"], f"Expected total_processed={truth['total_processed']}, got {data['total_processed']}"
    assert data["total_deduplicated"] == truth["total_deduplicated"], f"Expected total_deduplicated={truth['total_deduplicated']}, got {data['total_deduplicated']}"
    assert data["total_anomalies"] == truth["total_anomalies"], f"Expected total_anomalies={truth['total_anomalies']}, got {data['total_anomalies']}"

def test_api_anomalies(wait_for_service):
    truth = get_ground_truth()

    resp = requests.get("http://127.0.0.1:8080/api/anomalies", timeout=5)
    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Response from /api/anomalies is not valid JSON")

    assert isinstance(data, list), "Response from /api/anomalies should be a list"

    # Compare timestamps (as strings)
    assert data == truth["anomalies"], f"Anomalies mismatch. Expected {truth['anomalies']}, got {data}"