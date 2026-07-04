# test_final_state.py

import os
import stat
import subprocess
import random
import time
import urllib.request
import urllib.error
import json
import pytest

def test_directory_permissions_and_symlink():
    metrics_dir = "/home/user/metrics_data"
    raw_dir = "/home/user/metrics_data/raw"
    symlink_path = "/home/user/active_metrics"

    assert os.path.isdir(metrics_dir), f"Directory {metrics_dir} does not exist"
    assert os.path.isdir(raw_dir), f"Directory {raw_dir} does not exist"

    # Check permissions 0700 for metrics_dir and its subdirectories
    for d in [metrics_dir, raw_dir]:
        st = os.stat(d)
        perms = stat.S_IMODE(st.st_mode)
        assert perms == 0o700, f"Permissions of {d} are {oct(perms)}, expected 0o700"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"
    target = os.readlink(symlink_path)
    assert target == raw_dir, f"Symlink points to {target}, expected {raw_dir}"

def test_nginx_and_flask_ingestion():
    # Send a request to the ingest endpoint
    url = "http://127.0.0.1:8080/ingest"
    test_payload = {
        "timestamp": int(time.time()),
        "service": "test_service",
        "metric": "test_metric",
        "value": 42.5
    }
    data = json.dumps(test_payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status in [200, 201, 202], f"Unexpected status code: {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to reach Nginx on port 8080: {e}")

    # Allow some time for the log to be written
    time.sleep(1)

    raw_dir = "/home/user/metrics_data/raw"
    log_files = [f for f in os.listdir(raw_dir) if os.path.isfile(os.path.join(raw_dir, f))]
    assert log_files, f"No log files found in {raw_dir} after ingestion request"

    found = False
    for lf in log_files:
        with open(os.path.join(raw_dir, lf), "r") as f:
            content = f.read()
            if "test_service test_metric" in content or "test_service" in content:
                found = True
                break
    assert found, "Test metric data not found in any log file"

def test_planner_fuzz_equivalence():
    planner_path = "/home/user/planner.py"
    oracle_path = "/app/oracle_planner"

    assert os.path.isfile(planner_path), f"Missing {planner_path}"
    assert os.access(planner_path, os.X_OK), f"{planner_path} is not executable"

    # Check shebang
    with open(planner_path, "r") as f:
        first_line = f.readline().strip()
        assert first_line == "#!/usr/bin/env python3", f"Incorrect shebang in {planner_path}"

    random.seed(42)
    services = ['frontend', 'backend', 'db', 'cache', 'auth']
    metrics = ['cpu', 'mem', 'disk', 'net']

    for i in range(500):
        num_lines = random.randint(0, 100)
        lines = []
        for _ in range(num_lines):
            ts = random.randint(1600000000, 1700000000)
            svc = random.choice(services)
            met = random.choice(metrics)
            val = round(random.uniform(-50.0, 200.0), 2)
            lines.append(f"{ts} {svc} {met} {val}")

        input_data = "\n".join(lines) + "\n" if lines else ""
        input_bytes = input_data.encode("utf-8")

        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_path], input=input_bytes, capture_output=True
        )
        assert proc_oracle.returncode == 0, f"Oracle failed on iteration {i}"
        oracle_out = proc_oracle.stdout.decode("utf-8")

        # Run agent
        proc_agent = subprocess.run(
            [planner_path], input=input_bytes, capture_output=True
        )
        assert proc_agent.returncode == 0, f"Agent script failed on iteration {i}:\n{proc_agent.stderr.decode('utf-8')}"
        agent_out = proc_agent.stdout.decode("utf-8")

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"Input:\n{input_data}\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}"
            )