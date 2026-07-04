# test_final_state.py

import os
import socket
import time
import json
import subprocess
import requests
import pytest

def get_canonical_id(raw_id: int) -> int:
    """Use the actual binary to get the canonical ID to avoid re-implementing C logic."""
    process = subprocess.Popen(
        ['/app/id_mapper'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    stdout, _ = process.communicate(input=f"{raw_id}\n")
    return int(stdout.strip())

def test_pipeline_processing():
    # 1. Generate test data
    test_data = [
        {"raw_id": 1050, "duration": 42},
        {"raw_id": 1050, "duration": 10},
        {"raw_id": 9999, "duration": 100},
        {"raw_id": 123456, "duration": 5},
    ]

    # Calculate expected aggregations
    expected_aggregations = {}
    for item in test_data:
        canon_id = get_canonical_id(item["raw_id"])
        expected_aggregations[canon_id] = expected_aggregations.get(canon_id, 0) + item["duration"]

    # 2. Send data to TCP server
    csv_lines = []
    for item in test_data:
        csv_lines.append(f"2023-10-10T10:00:00Z,{item['raw_id']},action,{item['duration']}\n")

    payload = "".join(csv_lines).encode('utf-8')

    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=5) as sock:
            sock.sendall(payload)
    except ConnectionRefusedError:
        pytest.fail("TCP server is not listening on 127.0.0.1:9000")
    except Exception as e:
        pytest.fail(f"Failed to send data to TCP server: {e}")

    # 3. Wait for processing
    time.sleep(2)

    # 4. Verify HTTP API
    for canon_id, expected_duration in expected_aggregations.items():
        try:
            resp = requests.get(f"http://127.0.0.1:9001/aggregate?id={canon_id}", timeout=5)
            assert resp.status_code == 200, f"Expected HTTP 200, got {resp.status_code} for id {canon_id}"

            data = resp.json()
            assert "canonical_id" in data, f"Response missing 'canonical_id': {data}"
            assert "total_duration" in data, f"Response missing 'total_duration': {data}"

            assert int(data["canonical_id"]) == canon_id, f"Expected canonical_id {canon_id}, got {data['canonical_id']}"
            assert int(data["total_duration"]) >= expected_duration, f"Expected total_duration >= {expected_duration}, got {data['total_duration']}"
        except requests.exceptions.ConnectionError:
            pytest.fail("HTTP API server is not listening on 127.0.0.1:9001")

    # Also test an unseen ID
    unseen_id = 9999999
    resp = requests.get(f"http://127.0.0.1:9001/aggregate?id={unseen_id}", timeout=5)
    assert resp.status_code == 200
    data = resp.json()
    assert int(data["canonical_id"]) == unseen_id
    assert int(data["total_duration"]) == 0, f"Expected total_duration 0 for unseen id, got {data['total_duration']}"

def test_cron_job_configured():
    try:
        # Check crontab for 'user' (assuming we are running as user or root)
        # If running as root, we can check `crontab -l -u user` or just `crontab -l` if running as user.
        # Let's try both or just read the spool file.
        spool_file = "/var/spool/cron/crontabs/user"
        if os.path.exists(spool_file):
            with open(spool_file, "r") as f:
                crontab_content = f.read()
        else:
            # Fallback to crontab -l
            process = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            crontab_content = process.stdout

        assert "* * * * *" in crontab_content, "Cron job does not seem to be configured to run every minute (* * * * *)"
        assert "snapshot.json" in crontab_content, "Cron job does not reference snapshot.json"
    except Exception as e:
        pytest.fail(f"Failed to verify cron job: {e}")