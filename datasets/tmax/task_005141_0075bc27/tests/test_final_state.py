# test_final_state.py
import os
import json
import tarfile
import requests
import time
import pytest

BASE_URL = "http://127.0.0.1:8333"
LOG_DIR = "/app/live_logs"
ACTIVE_LOG = os.path.join(LOG_DIR, "active.jsonl")
ROTATED_LOG = os.path.join(LOG_DIR, "active.jsonl.1")

def test_backup_and_stats():
    # 1. Wait for server to start
    for _ in range(30):
        try:
            requests.get(f"{BASE_URL}/stats", timeout=1)
            break
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    else:
        pytest.fail("Server did not start or become reachable on port 8333 within 15 seconds.")

    # 2. Write 5 JSON objects to active log
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(ACTIVE_LOG, "w") as f:
        for i in range(5):
            f.write(json.dumps({"line": i}) + "\n")

    # 3. Send POST /backup
    try:
        resp = requests.post(f"{BASE_URL}/backup", timeout=10)
        assert resp.status_code == 200, f"Expected 200 OK for first /backup, got {resp.status_code}: {resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"POST /backup failed: {e}")

    # 4. Simulate rotation
    if os.path.exists(ACTIVE_LOG):
        os.rename(ACTIVE_LOG, ROTATED_LOG)

    # 5. Write 4 JSON objects to new active log
    with open(ACTIVE_LOG, "w") as f:
        for i in range(5, 9):
            f.write(json.dumps({"line": i}) + "\n")

    # 6. Send POST /backup
    try:
        resp = requests.post(f"{BASE_URL}/backup", timeout=10)
        assert resp.status_code == 200, f"Expected 200 OK for second /backup, got {resp.status_code}: {resp.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"POST /backup failed: {e}")

    # 7. Send GET /stats
    try:
        resp = requests.get(f"{BASE_URL}/stats", timeout=10)
        assert resp.status_code == 200, f"Expected 200 OK for /stats, got {resp.status_code}: {resp.text}"
        stats = resp.json()
    except requests.exceptions.RequestException as e:
        pytest.fail(f"GET /stats failed: {e}")
    except ValueError:
        pytest.fail(f"GET /stats did not return valid JSON. Response: {resp.text}")

    # 8. Assert stats
    assert stats.get("total_backed_up_lines") == 9, f"Expected 9 backed up lines, got {stats.get('total_backed_up_lines')}"
    assert stats.get("total_keyframes") == 11, f"Expected 11 keyframes, got {stats.get('total_keyframes')}"

    # Verify frames.csv exists
    assert os.path.exists("/home/user/frames.csv"), "Missing /home/user/frames.csv"

    # Verify archive exists and contains exactly 4 log lines
    archive_path = "/home/user/archive/backup_2.tar.gz"
    assert os.path.exists(archive_path), f"Missing archive {archive_path}"

    # Unpack and verify
    extracted_lines = 0
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            for member in tar.getmembers():
                if member.isfile() and not member.name.endswith("frames.csv"):
                    f = tar.extractfile(member)
                    if f:
                        content = f.read().decode("utf-8").strip()
                        if content:
                            extracted_lines += len(content.split("\n"))
    except tarfile.TarError as e:
        pytest.fail(f"Failed to read tar archive {archive_path}: {e}")

    assert extracted_lines == 4, f"Expected exactly 4 log lines in backup_2.tar.gz, found {extracted_lines}"