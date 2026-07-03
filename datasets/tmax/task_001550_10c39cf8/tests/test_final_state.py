# test_final_state.py

import os
import json
import time
import subprocess
import pytest

LOG_FILE = "/home/user/observability/logs/access.log"
OUT_FILE = "/home/user/observability/metrics/summary.json"
COLLECTOR = "/home/user/observability/collector.sh"

def generate_log_file(num_lines=500_000):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    line_200 = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET / HTTP/1.1" 200 1024\n'
    line_301 = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET / HTTP/1.1" 301 0\n'
    line_404 = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET / HTTP/1.1" 404 512\n'
    line_500 = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET / HTTP/1.1" 500 256\n'

    # 10 lines per pattern block
    pattern = (line_200 * 7) + (line_301 * 1) + (line_404 * 1) + (line_500 * 1)

    with open(LOG_FILE, "w") as f:
        for _ in range(num_lines // 10):
            f.write(pattern)

    expected = {
        "status_2xx": (num_lines // 10) * 7,
        "status_3xx": (num_lines // 10) * 1,
        "status_4xx": (num_lines // 10) * 1,
        "status_5xx": (num_lines // 10) * 1,
        "total_bytes": (num_lines // 10) * (7 * 1024 + 1 * 0 + 1 * 512 + 1 * 256)
    }
    return expected

def test_collector_performance_and_correctness():
    expected = generate_log_file(500_000)

    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)

    start_time = time.time()
    result = subprocess.run(
        ["bash", COLLECTOR],
        env={"PWD": "/tmp"},
        cwd="/tmp",
        capture_output=True,
        text=True
    )
    end_time = time.time()

    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    duration = end_time - start_time
    assert duration <= 1.5, f"Execution time {duration:.2f}s exceeded threshold of 1.5s. Optimize your script (e.g. using awk)."

    assert os.path.exists(OUT_FILE), f"Output file {OUT_FILE} was not created. Ensure you are using absolute paths."

    with open(OUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON")

    assert data.get("status_2xx") == expected["status_2xx"], f"status_2xx mismatch: {data.get('status_2xx')} != {expected['status_2xx']}"
    assert data.get("status_3xx") == expected["status_3xx"], f"status_3xx mismatch: {data.get('status_3xx')} != {expected['status_3xx']}"
    assert data.get("status_4xx") == expected["status_4xx"], f"status_4xx mismatch: {data.get('status_4xx')} != {expected['status_4xx']}"
    assert data.get("status_5xx") == expected["status_5xx"], f"status_5xx mismatch: {data.get('status_5xx')} != {expected['status_5xx']}"
    assert data.get("total_bytes") == expected["total_bytes"], f"total_bytes mismatch: {data.get('total_bytes')} != {expected['total_bytes']}"

def test_empty_log_file():
    with open(LOG_FILE, "w") as f:
        f.write("")

    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)

    result = subprocess.run(
        ["bash", COLLECTOR],
        env={"PWD": "/tmp"},
        cwd="/tmp",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on empty log with error: {result.stderr}"
    assert os.path.exists(OUT_FILE), f"Output file {OUT_FILE} was not created for empty log."

    with open(OUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file for empty log is not valid JSON")

    for key in ["status_2xx", "status_3xx", "status_4xx", "status_5xx", "total_bytes"]:
        assert data.get(key) == 0, f"{key} should be 0 for empty log, got {data.get(key)}"