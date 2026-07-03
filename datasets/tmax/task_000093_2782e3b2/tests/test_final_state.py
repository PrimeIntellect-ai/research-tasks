# test_final_state.py

import os
import subprocess
import time
import pytest

def test_build_and_executable():
    build_script = '/home/user/build.sh'
    supervisor_bin = '/home/user/supervisor'

    assert os.path.isfile(build_script), f"Build script {build_script} does not exist."

    # Run the build script
    try:
        subprocess.run(['bash', build_script], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Build script failed with exit code {e.returncode}. stderr: {e.stderr}")

    assert os.path.isfile(supervisor_bin), f"Compiled binary {supervisor_bin} does not exist after running build script."
    assert os.access(supervisor_bin, os.X_OK), f"Compiled binary {supervisor_bin} is not executable."

def test_supervisor_performance_and_correctness():
    supervisor_bin = '/home/user/supervisor'
    test_data = '/app/test_data.txt'
    log_path = '/home/user/logs/test.log'
    log_rotated = '/home/user/logs/test.log.1'

    assert os.path.isfile(test_data), f"Test data {test_data} missing."

    # Clean up previous logs if any
    for p in [log_path, log_rotated]:
        if os.path.exists(p):
            os.remove(p)

    env = os.environ.copy()
    env['WORKER_COUNT'] = '8'
    env['LOG_PATH'] = log_path

    start_time = time.time()
    with open(test_data, 'r') as f_in:
        process = subprocess.Popen(
            [supervisor_bin],
            stdin=f_in,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        stdout, stderr = process.communicate()
    end_time = time.time()

    duration = end_time - start_time

    # Check metric
    assert duration <= 4.0, f"Execution time {duration:.2f}s exceeded threshold of 4.0s"

    # Check correctness
    lines_processed = 0
    for path in [log_path, log_rotated]:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    if line.startswith("PROCESSED:"):
                        lines_processed += 1

    assert lines_processed >= 1900, f"Expected at least 1900 processed lines, got {lines_processed}."

    # Check if log rotation happened
    assert os.path.exists(log_rotated), f"Log rotation failed: {log_rotated} does not exist."
    assert os.path.exists(log_path), f"Log rotation failed: {log_path} does not exist."