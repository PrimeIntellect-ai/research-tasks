# test_final_state.py

import os
import subprocess
import time
import uuid
import pytest

SCRIPT_PATH = "/home/user/final_filter.sh"

def test_final_filter_exists():
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is missing. Did you copy the fixed script?"

def test_filter_adversarial_corpus():
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is missing."

    clean_file = "/app/corpora/clean/logs.txt"
    evil_file = "/app/corpora/evil/logs.txt"

    assert os.path.isfile(clean_file), f"Clean corpus missing at {clean_file}"
    assert os.path.isfile(evil_file), f"Evil corpus missing at {evil_file}"

    with open(clean_file, "r") as f:
        clean_lines = [line for line in f.read().splitlines() if line.strip()]

    with open(evil_file, "r") as f:
        evil_lines = [line for line in f.read().splitlines() if line.strip()]

    failed_clean = []
    for line in clean_lines:
        proc = subprocess.run(["bash", SCRIPT_PATH], input=line + "\n", text=True, capture_output=True)
        if proc.stdout.strip() != line.strip():
            failed_clean.append(line)

    failed_evil = []
    for line in evil_lines:
        proc = subprocess.run(["bash", SCRIPT_PATH], input=line + "\n", text=True, capture_output=True)
        if proc.stdout.strip() != "":
            failed_evil.append(line)

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_lines)} clean lines modified or rejected. Examples: {failed_clean[:3]}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_lines)} evil lines bypassed the filter. Examples: {failed_evil[:3]}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_pipeline_active():
    # Append a unique canary log that is VALID to the dummy logs
    canary_id = str(uuid.uuid4())[:8]
    # Format: YYYY-MM-DD HH:MM:SS [LEVEL] Metric=<number>
    canary_line = f"2023-10-12 10:00:00 [INFO] Metric=50 Canary={canary_id}"

    with open("/app/dummy_logs.txt", "a") as f:
        f.write(canary_line + "\n")

    # Wait for the agent's background pipeline to process the new log
    # It should continuously or periodically reconnect to port 8001
    found = False
    out_file = "/tmp/pipeline_out.log"

    for _ in range(15):
        if os.path.isfile(out_file):
            with open(out_file, "r") as f:
                content = f.read()
                if canary_id in content:
                    found = True
                    break
        time.sleep(1)

    assert found, (
        f"Canary log was not found in {out_file} after 15 seconds. "
        "Ensure your background pipeline is continuously reading from port 8001, "
        "filtering, and writing to port 8002."
    )