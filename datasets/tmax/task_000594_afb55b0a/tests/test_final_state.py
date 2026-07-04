# test_final_state.py

import os
import time
import subprocess
import pytest

def test_libraries_built():
    """Verify that the static C library and the shared Go library have been built."""
    assert os.path.isfile("/app/fastcrc-1.0/libfastcrc.a"), "The static library /app/fastcrc-1.0/libfastcrc.a was not built."
    assert os.path.isfile("/app/gocrc/libgocrc.so"), "The shared library /app/gocrc/libgocrc.so was not built."

def test_process_uploads_exists():
    """Verify that the Python integration script exists."""
    assert os.path.isfile("/home/user/process_uploads.py"), "/home/user/process_uploads.py does not exist."

def test_correctness_and_performance():
    """Verify the output matches baseline and the speedup is >= 1.5."""

    # Run baseline
    t0 = time.time()
    result_base = subprocess.run(
        ["python3", "/app/baseline.py"],
        capture_output=True,
        text=True,
        check=True
    )
    t_base = time.time() - t0
    baseline_output = result_base.stdout.strip()

    # Run agent script
    t0 = time.time()
    result_agent = subprocess.run(
        ["python3", "/home/user/process_uploads.py"],
        capture_output=True,
        text=True,
        check=True
    )
    t_agent = time.time() - t0
    agent_output = result_agent.stdout.strip()

    # Check correctness
    assert agent_output == baseline_output, f"Agent output '{agent_output}' does not match baseline output '{baseline_output}'."

    # Check performance
    speedup = t_base / t_agent
    assert speedup >= 1.5, f"Speedup is {speedup:.2f}x, which is below the 1.5x threshold. (Agent time: {t_agent:.2f}s, Baseline time: {t_base:.2f}s)"