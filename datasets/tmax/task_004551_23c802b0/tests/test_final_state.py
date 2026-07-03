# test_final_state.py

import os
import time
import subprocess
import glob

def test_process_all_performance():
    script_path = "/home/user/process_all.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Ensure the directory exists (agent should have created it and the 500 files)
    raw_dir = "/home/user/manifests/raw/"
    assert os.path.exists(raw_dir), f"Directory {raw_dir} does not exist."

    # Measure execution time
    start = time.time()
    proc = subprocess.run(["/bin/bash", script_path], capture_output=True, text=True)
    end = time.time()

    execution_time = end - start
    optimized_files = glob.glob(os.path.join(raw_dir, "*.opt.yaml"))

    assert proc.returncode == 0, f"Script failed to execute with return code {proc.returncode}.\nstdout: {proc.stdout}\nstderr: {proc.stderr}"
    assert len(optimized_files) >= 500, f"Did not process 500 manifests. Found {len(optimized_files)} optimized files."
    assert execution_time <= 10.0, f"Execution time {execution_time:.2f} exceeds threshold of 10.0s."