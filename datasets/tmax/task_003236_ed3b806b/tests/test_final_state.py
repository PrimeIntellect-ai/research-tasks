# test_final_state.py
import os
import subprocess
import json
import hashlib
import csv
from datetime import datetime, timedelta

def test_detector_clean_corpus():
    clean_dir = "/app/corpora/clean"
    detector_script = "/home/user/detector.py"
    assert os.path.isfile(detector_script), "detector.py not found"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    bypassed = []

    for f in clean_files:
        path = os.path.join(clean_dir, f)
        res = subprocess.run(["python3", detector_script, path], capture_output=True)
        if res.returncode != 0:
            bypassed.append(f)

    assert not bypassed, f"{len(bypassed)} of {len(clean_files)} clean modified/rejected: {bypassed}"

def test_detector_evil_corpus():
    evil_dir = "/app/corpora/evil"
    detector_script = "/home/user/detector.py"
    assert os.path.isfile(detector_script), "detector.py not found"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    bypassed = []

    for f in evil_files:
        path = os.path.join(evil_dir, f)
        res = subprocess.run(["python3", detector_script, path], capture_output=True)
        if res.returncode != 1:
            bypassed.append(f)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {bypassed}"

def test_etl_timeline():
    timeline_path = "/home/user/timeline.csv"
    assert os.path.isfile(timeline_path), f"{timeline_path} not found"

    with open(timeline_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "timeline.csv is empty"
    assert rows[0] == ["bucket_start", "server_id", "config_hash"], "Invalid CSV header"

    data = rows[1:]

    salt = "k9#xP2m"

    payload_srv1 = {"path": "/var/www/html", "service": "web", "workers": 4}
    json_srv1 = json.dumps(payload_srv1, separators=(',', ':'), sort_keys=True)
    hash_srv1 = hashlib.sha256((json_srv1 + salt).encode()).hexdigest()

    payload_srv2 = {"options": ["--bind", "0.0.0.0"], "service": "db"}
    json_srv2 = json.dumps(payload_srv2, separators=(',', ':'), sort_keys=True)
    hash_srv2 = hashlib.sha256((json_srv2 + salt).encode()).hexdigest()

    start_time = datetime(2024, 1, 1, 0, 0, 0)
    buckets = []
    for i in range(48):
        buckets.append((start_time + timedelta(minutes=30*i)).strftime("%Y-%m-%dT%H:%M:%SZ"))

    expected_rows = []
    for b in buckets:
        if b == "2024-01-01T00:00:00Z":
            expected_rows.append([b, "srv1", "EMPTY"])
        else:
            expected_rows.append([b, "srv1", hash_srv1])

        if b < "2024-01-01T02:00:00Z":
            expected_rows.append([b, "srv2", "EMPTY"])
        else:
            expected_rows.append([b, "srv2", hash_srv2])

    expected_rows.sort(key=lambda x: (x[0], x[1]))

    assert len(data) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(data)}"
    for i in range(len(expected_rows)):
        assert data[i] == expected_rows[i], f"Mismatch at row {i+1}: expected {expected_rows[i]}, got {data[i]}"