# test_final_state.py

import os
import time
import subprocess
import glob

def test_scheduler_runtime_and_logs():
    scheduler_path = "/home/user/scheduler.py"
    assert os.path.exists(scheduler_path), f"Scheduler script not found at {scheduler_path}"

    # Measure runtime
    start_time = time.time()
    result = subprocess.run(
        ["python3", scheduler_path],
        capture_output=True,
        text=True
    )
    end_time = time.time()
    runtime = end_time - start_time

    assert result.returncode == 0, f"Scheduler exited with non-zero status. Stderr: {result.stderr}"

    # Metric threshold check
    threshold = 9.5
    assert runtime <= threshold, (
        f"Scheduler runtime was {runtime:.2f}s, which exceeds the threshold of {threshold}s. "
        "Ensure tasks are correctly parallelized according to the DAG."
    )

    # Verify logs exist
    logs_dir = "/home/user/logs"
    assert os.path.exists(logs_dir), f"Logs directory not found at {logs_dir}"

    for task in ["A", "B", "C", "D", "E"]:
        # Check for either the base log file or rotated compressed logs
        base_log = os.path.join(logs_dir, f"task_{task}.log")
        rotated_logs = glob.glob(os.path.join(logs_dir, f"task_{task}.log*.gz"))

        log_exists = os.path.exists(base_log) or len(rotated_logs) > 0
        assert log_exists, f"No log files found for task {task} in {logs_dir}"