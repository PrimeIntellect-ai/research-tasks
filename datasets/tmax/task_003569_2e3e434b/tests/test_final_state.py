# test_final_state.py
import os
import time
import json
import zipfile
import subprocess
import threading
import fcntl
import pytest

def writer_thread(stop_event):
    """Continuously writes a 5MB JSON payload with exclusive locking."""
    # Create a ~5MB JSON payload
    data = {"status": "active", "payload": "X" * (5 * 1024 * 1024 - 50)}
    json_str = json.dumps(data)
    filepath = "/home/user/config/live.json"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    while not stop_event.is_set():
        with open(filepath, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(json_str)
            f.flush()
            fcntl.flock(f, fcntl.LOCK_UN)
        time.sleep(0.005)

def test_safe_archiver_performance_and_correctness():
    """
    Validates the safe_archiver executable.
    It must produce 50 valid zip files of the JSON config while a background
    writer is constantly updating it. The average time per valid snapshot
    must be <= 15.0 ms.
    """
    archiver_path = "/home/user/safe_archiver"
    input_file = "/home/user/config/live.json"
    output_dir = "/home/user/backups"

    assert os.path.isfile(archiver_path), f"Archiver executable not found at {archiver_path}"

    os.makedirs(output_dir, exist_ok=True)

    # Clean up any existing backups
    for f in os.listdir(output_dir):
        if f.endswith(".zip"):
            os.remove(os.path.join(output_dir, f))

    stop_event = threading.Event()
    writer = threading.Thread(target=writer_thread, args=(stop_event,))
    writer.start()

    # Wait for the writer to create the initial file
    while not os.path.exists(input_file):
        time.sleep(0.01)

    start_time = time.time()

    try:
        proc = subprocess.run(
            [archiver_path, input_file, output_dir], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        assert proc.returncode == 0, f"Archiver failed with return code {proc.returncode}. Stderr: {proc.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("Archiver timed out after 30 seconds. This indicates it is either deadlocked or too slow.")
    finally:
        stop_event.set()
        writer.join()

    execution_time_ms = (time.time() - start_time) * 1000.0

    valid_count = 0
    for i in range(50):
        zip_path = os.path.join(output_dir, f"snap_{i}.zip")
        if not os.path.exists(zip_path):
            continue

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                files = zf.namelist()
                if not files:
                    continue
                with zf.open(files[0]) as f:
                    content = f.read().decode('utf-8')
                    # If it parses successfully, it's valid (no tearing)
                    json.loads(content)
                    valid_count += 1
        except Exception:
            # Parse error, bad zip, etc.
            pass

    assert valid_count > 0, "No valid JSON archives were produced. Locking or compression failed completely."

    metric = execution_time_ms / valid_count

    assert metric <= 15.0, (
        f"Valid Snapshot Time metric failed: {metric:.2f} ms per valid snapshot. "
        f"Threshold is <= 15.0 ms. Valid count: {valid_count}/50, "
        f"Total time: {execution_time_ms:.2f} ms. "
        f"Ensure miniz is compiled with optimizations and mmap is used."
    )