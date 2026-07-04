# test_final_state.py
import os
import shutil
import time
import subprocess
import json
import pytest

def test_speedup_and_correctness():
    """
    Measures execution speedup of fast_organizer.py over slow_organizer.py,
    ensuring it meets the >= 5.0x threshold and correctly classifies files.
    """
    # Restore files to /app/uploads in case the agent or previous runs moved them
    for d in ["/app/safe", "/app/quarantine"]:
        if os.path.exists(d):
            for f in os.listdir(d):
                shutil.move(os.path.join(d, f), os.path.join("/app/uploads", f))

    uploads_count = len(os.listdir("/app/uploads"))
    assert uploads_count == 20000, f"Expected 20000 files in /app/uploads, but found {uploads_count}."

    # Ensure the required scripts exist
    assert os.path.isfile("/app/slow_organizer.py"), "/app/slow_organizer.py is missing."
    assert os.path.isfile("/app/fast_organizer.py"), "/app/fast_organizer.py is missing."

    # 1. Run slow baseline
    start_slow = time.time()
    subprocess.run(["python3", "/app/slow_organizer.py"], check=True, cwd="/app")
    slow_duration = time.time() - start_slow

    # 2. Run agent's fast implementation
    start_fast = time.time()
    subprocess.run(["python3", "/app/fast_organizer.py"], check=True, cwd="/app")
    fast_duration = time.time() - start_fast

    speedup = slow_duration / fast_duration

    # 3. Verify correctness
    assert os.path.isfile("/app/slow_results.json"), "/app/slow_results.json was not generated."
    assert os.path.isfile("/app/results.json"), "/app/results.json was not generated."

    with open("/app/slow_results.json") as f:
        slow_res = json.load(f)
    with open("/app/results.json") as f:
        fast_res = json.load(f)

    assert slow_res["safe_count"] == fast_res["safe_count"], \
        f"Safe counts do not match. Slow: {slow_res['safe_count']}, Fast: {fast_res['safe_count']}"
    assert slow_res["quarantine_count"] == fast_res["quarantine_count"], \
        f"Quarantine counts do not match. Slow: {slow_res['quarantine_count']}, Fast: {fast_res['quarantine_count']}"

    safe_dir_count = len(os.listdir("/app/safe"))
    quarantine_dir_count = len(os.listdir("/app/quarantine"))

    assert safe_dir_count == fast_res["safe_count"], \
        f"Files were not moved to /app/safe correctly. Expected {fast_res['safe_count']}, found {safe_dir_count}."
    assert quarantine_dir_count == fast_res["quarantine_count"], \
        f"Files were not moved to /app/quarantine correctly. Expected {fast_res['quarantine_count']}, found {quarantine_dir_count}."

    # 4. Enforce metric threshold
    assert speedup >= 5.0, f"Speedup was {speedup:.2f}x, which is less than the required 5.0x threshold."