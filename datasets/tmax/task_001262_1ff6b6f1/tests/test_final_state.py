# test_final_state.py
import os
import subprocess
import requests
import concurrent.futures
import zipfile
import io
import csv
import re

def get_expected_frame_count():
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-count_frames", "-show_entries", "stream=nb_read_frames",
        "-of", "csv=p=0", "/app/surveillance.mp4"
    ]
    try:
        output = subprocess.check_output(cmd).decode().strip()
        return int(output)
    except Exception:
        return None

def test_server_functionality():
    base_url = "http://127.0.0.1:8080"

    # 1. POST /analyze
    try:
        resp_analyze = requests.post(f"{base_url}/analyze", timeout=10)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to /analyze: {e}"

    assert resp_analyze.status_code == 200, f"Expected 200 OK from /analyze, got {resp_analyze.status_code}"

    # 2. 50 concurrent POST /log
    def send_log(i):
        payload = {"timestamp": str(1000 + i), "event": f"Concurrent event {i}"}
        try:
            resp = requests.post(f"{base_url}/log", json=payload, timeout=5)
            return resp.status_code, payload
        except Exception as e:
            return 0, payload

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(send_log, i) for i in range(50)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    for status, payload in results:
        assert status == 200, f"Expected 200 OK from /log for {payload}, got {status}"

    # 3. GET /backup
    try:
        resp_backup = requests.get(f"{base_url}/backup", timeout=10)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to /backup: {e}"

    assert resp_backup.status_code == 200, f"Expected 200 OK from /backup, got {resp_backup.status_code}"
    assert "zip" in resp_backup.headers.get("Content-Type", "").lower(), "Response Content-Type should indicate a zip file"

    # 4. Verify ZIP integrity and contents
    try:
        z = zipfile.ZipFile(io.BytesIO(resp_backup.content))
    except zipfile.BadZipFile:
        assert False, "Response body is not a valid ZIP file"

    namelist = z.namelist()
    assert "video_events.csv" in namelist, "video_events.csv not found at the root of the backup ZIP"
    assert "surveillance.mp4" in namelist, "surveillance.mp4 not found at the root of the backup ZIP"

    # 5. Verify CSV contents (ensuring file locking prevented corruption)
    with z.open("video_events.csv") as f:
        content = f.read().decode("utf-8")

    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)

    assert len(rows) == 51, f"Expected exactly 51 rows in CSV (1 analyze + 50 logs), found {len(rows)}"

    # Check first row (analyze result)
    first_row = rows[0]
    assert first_row.get("timestamp") == "0", f"First row timestamp should be '0', got {first_row.get('timestamp')}"

    expected_frames = get_expected_frame_count()
    event_text = first_row.get("event", "")
    if expected_frames is not None:
        assert str(expected_frames) in event_text, f"Expected frame count {expected_frames} in event: '{event_text}'"
    else:
        assert re.search(r"Video contains \d+ frames", event_text), f"First row event does not match expected format: '{event_text}'"

    # Check concurrent logs
    events = [r.get("event", "") for r in rows[1:]]
    for i in range(50):
        expected_event = f"Concurrent event {i}"
        assert expected_event in events, f"Missing '{expected_event}' in CSV. Concurrency issue or missing log."