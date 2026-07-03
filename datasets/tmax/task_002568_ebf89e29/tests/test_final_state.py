# test_final_state.py

import os
import subprocess
import time
import random
import pytest

def test_files_exist():
    assert os.path.exists("/home/user/fast_filter.cpp"), "Missing /home/user/fast_filter.cpp"
    assert os.path.exists("/home/user/pipeline.sh"), "Missing /home/user/pipeline.sh"

def test_cron_job_configured():
    try:
        # Check root or user crontab
        try:
            output = subprocess.check_output(["crontab", "-l"], text=True, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            output = subprocess.check_output(["crontab", "-l", "-u", "user"], text=True, stderr=subprocess.DEVNULL)

        assert "5" in output, "Cron job does not appear to run every 5 minutes"
        assert "incoming" in output or "fast_filter" in output or "pipeline.sh" in output, "Cron job does not seem to reference the required script or directories"
    except Exception as e:
        pytest.fail(f"Could not verify cron job: {e}")

def test_fast_filter_performance_and_accuracy():
    # Ensure the executable exists. If not, try running the pipeline script.
    fast_bin = "/home/user/fast_filter"
    if not os.path.exists(fast_bin):
        subprocess.run(["bash", "/home/user/pipeline.sh"], check=False)

    assert os.path.exists(fast_bin), f"Executable {fast_bin} not found. Ensure pipeline.sh compiles it."
    assert os.access(fast_bin, os.X_OK), f"{fast_bin} is not executable."

    input_file = "/tmp/test_data.csv"
    legacy_out = "/tmp/legacy_out.csv"
    fast_out = "/tmp/fast_out.csv"

    # Generate test data (100,000 rows to keep test time reasonable while still measuring speedup)
    num_rows = 100000
    with open(input_file, 'w') as f:
        f.write("id,category,v1,v2,v3\n")
        for i in range(num_rows):
            cat = f"cat{i % 50}"
            v1 = random.uniform(0, 10)
            v2 = random.uniform(0, 10)
            # Make ~50% of rows valid
            v3 = (v1*v1 + v2*v2) + random.uniform(-50, 50)
            f.write(f"{i},{cat},{v1:.4f},{v2:.4f},{v3:.4f}\n")

    # Measure legacy
    t0 = time.time()
    subprocess.run(["/app/legacy_filter", input_file, legacy_out], check=True)
    legacy_time = time.time() - t0

    # Measure fast
    t0 = time.time()
    subprocess.run([fast_bin, input_file, fast_out], check=True)
    fast_time = time.time() - t0

    # Verify Exact Match
    with open(legacy_out, 'r') as f1, open(fast_out, 'r') as f2:
        legacy_content = f1.read()
        fast_content = f2.read()

    assert legacy_content == fast_content, "Outputs do not match exactly! The fast_filter output differs from legacy_filter."

    # Verify Speedup
    speedup = legacy_time / max(fast_time, 1e-6)
    assert speedup >= 4.0, f"Speedup {speedup:.2f}x is less than threshold 4.0x (Legacy: {legacy_time:.3f}s, Fast: {fast_time:.3f}s)"