# test_final_state.py

import os
import time
import subprocess
import pytest

def test_telemetry_log_exists():
    log_path = "/home/user/telemetry.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run the telemetry generator?"

    # Check if it has a reasonable size (2.5 million lines is roughly 70-80MB)
    size = os.path.getsize(log_path)
    assert size > 50_000_000, f"Log file {log_path} is too small ({size} bytes). Did you redirect the full output?"

def test_code_committed():
    repo_path = "/home/user/repo"

    # Check if analyzer.cpp exists
    cpp_path = os.path.join(repo_path, "analyzer.cpp")
    assert os.path.isfile(cpp_path), f"Source file {cpp_path} does not exist."

    # Check if it is committed
    proc = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD", "--name-only"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert proc.returncode == 0, "Failed to run git ls-tree. Is there a valid commit?"
    assert "analyzer.cpp" in proc.stdout.splitlines(), "analyzer.cpp is not committed to the repository."

def test_analyzer_performance_and_correctness():
    cpp_path = "/home/user/repo/analyzer.cpp"
    bin_path = "/tmp/analyzer_perf"
    log_path = "/home/user/telemetry.log"

    # Compile the code
    compile_proc = subprocess.run(
        ["g++", "-O3", cpp_path, "-o", bin_path],
        capture_output=True,
        text=True
    )
    assert compile_proc.returncode == 0, f"Failed to compile {cpp_path}:\n{compile_proc.stderr}"

    # Run the performance test
    start_time = time.time()
    run_proc = subprocess.run(
        [bin_path, log_path, "vm-42"],
        capture_output=True,
        text=True
    )
    end_time = time.time()

    elapsed = end_time - start_time

    assert run_proc.returncode == 0, f"Analyzer crashed or returned non-zero exit code:\n{run_proc.stderr}"

    output = run_proc.stdout.strip()
    assert len(output) > 0, "Analyzer produced no output."

    try:
        avg_cpu = float(output)
    except ValueError:
        pytest.fail(f"Analyzer output '{output}' is not a valid floating-point number.")

    # The expected average should be around 49-50 since it's random 0-100
    assert 40.0 <= avg_cpu <= 60.0, f"Calculated average CPU ({avg_cpu}) seems incorrect. Expected ~50.0"

    # Check metric threshold
    threshold = 0.15
    assert elapsed <= threshold, f"Execution too slow: {elapsed:.4f}s (Must be <= {threshold}s). Optimize your I/O and parsing."