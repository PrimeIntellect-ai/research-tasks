# test_final_state.py

import os
import json
import urllib.request
import subprocess
import time
import pytest

def test_dashboard_summary():
    summary_file = "/home/user/dashboard-summary.txt"
    assert os.path.isfile(summary_file), f"File {summary_file} does not exist."
    with open(summary_file, "r") as f:
        content = f.read().strip()
    assert content == "TOTAL_ALICE=20", f"Expected 'TOTAL_ALICE=20', got '{content}'."

def test_metrics_logs_exist_and_counts():
    log_8081 = "/home/user/metrics_8081.log"
    log_8082 = "/home/user/metrics_8082.log"

    assert os.path.isfile(log_8081), f"Log file {log_8081} does not exist."
    assert os.path.isfile(log_8082), f"Log file {log_8082} does not exist."

    with open(log_8081, "r") as f:
        lines_8081 = [line.strip() for line in f if line.strip()]
    with open(log_8082, "r") as f:
        lines_8082 = [line.strip() for line in f if line.strip()]

    total_lines = len(lines_8081) + len(lines_8082)
    # We expect at least 3 from the commits. If the student ran it multiple times it might be more,
    # but based on the truth we expect exactly 3 lines total before our test POST.
    # However, let's just check the distribution for the first 3 or just all lines.
    assert total_lines >= 3, f"Expected at least 3 log entries, found {total_lines}."

    # Check that lengths are distributed (round robin implies difference of at most 1, or exactly 2 and 1 if 3 items)
    # If exactly 3 items:
    if total_lines == 3:
        assert (len(lines_8081) == 2 and len(lines_8082) == 1) or (len(lines_8081) == 1 and len(lines_8082) == 2), \
            "Round-robin load balancing failed: expected 2 lines in one log and 1 in the other."

    alice_lines = 0
    bob_lines = 0

    for line in lines_8081 + lines_8082:
        try:
            data = json.loads(line)
            if data.get("author") == "Alice":
                alice_lines += data.get("lines_added", 0)
            elif data.get("author") == "Bob":
                bob_lines += data.get("lines_added", 0)
        except json.JSONDecodeError:
            pass

    assert alice_lines >= 20, f"Expected Alice to have at least 20 lines added in logs, got {alice_lines}."
    assert bob_lines >= 10, f"Expected Bob to have at least 10 lines added in logs, got {bob_lines}."

def test_git_commits():
    repo_dir = "/home/user/telemetry.git"
    assert os.path.isdir(repo_dir), f"Bare repo {repo_dir} does not exist."

    # Get commits
    cmd = ["git", "-C", repo_dir, "log", "--format=%an", "--shortstat", "master"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run git log on bare repo."

    output = result.stdout.strip().split("\n")
    # Output format roughly:
    # Alice
    #  1 file changed, 15 insertions(+)
    # 
    # Bob
    #  1 file changed, 10 insertions(+)
    # 
    # Alice
    #  1 file changed, 5 insertions(+)

    alice_insertions = 0
    bob_insertions = 0

    current_author = None
    for line in output:
        line = line.strip()
        if not line:
            continue
        if line in ["Alice", "Bob"]:
            current_author = line
        elif "insertion" in line:
            parts = line.split(",")
            for p in parts:
                if "insertion" in p:
                    num = int(p.strip().split()[0])
                    if current_author == "Alice":
                        alice_insertions += num
                    elif current_author == "Bob":
                        bob_insertions += num

    assert alice_insertions >= 20, f"Expected Alice to have at least 20 insertions in git history, got {alice_insertions}."
    assert bob_insertions >= 10, f"Expected Bob to have at least 10 insertions in git history, got {bob_insertions}."

def test_load_balancer_live():
    # Send a test POST request to 8080 and verify it appears in one of the logs
    log_8081 = "/home/user/metrics_8081.log"
    log_8082 = "/home/user/metrics_8082.log"

    def get_log_lines():
        lines = []
        for log_file in [log_8081, log_8082]:
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    lines.extend(f.readlines())
        return lines

    initial_lines = get_log_lines()

    test_payload = json.dumps({"author": "TestUser", "lines_added": 999}).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8080", data=test_payload, headers={'Content-Type': 'application/json'}, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status in [200, 201, 202, 204], f"Unexpected status code {response.status}"
    except Exception as e:
        pytest.fail(f"Failed to send request to load balancer: {e}")

    time.sleep(1) # wait for log write

    final_lines = get_log_lines()
    assert len(final_lines) > len(initial_lines), "Test request did not appear in any backend log."

    found = False
    for line in final_lines[len(initial_lines):]:
        try:
            data = json.loads(line)
            if data.get("author") == "TestUser" and data.get("lines_added") == 999:
                found = True
                break
        except json.JSONDecodeError:
            pass

    assert found, "Test JSON payload was not found in the backend logs."