# test_final_state.py

import os
import subprocess
import time
import pytest

def test_frames_extracted():
    """Verify that frames were extracted from the video."""
    frames_dir = "/home/user/frames"
    assert os.path.isdir(frames_dir), "Frames directory /home/user/frames does not exist."
    jpg_files = [f for f in os.listdir(frames_dir) if f.endswith('.jpg')]
    assert len(jpg_files) > 0, "No .jpg files found in /home/user/frames."

def test_generate_trail_script():
    """Verify that the sandbox script exists and contains the required bwrap constraints."""
    script_path = "/home/user/generate_trail.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()
    assert "bwrap" in content, "bwrap command not found in generate_trail.sh"
    assert "--unshare-net" in content, "--unshare-net constraint not found in generate_trail.sh"

def test_audit_trail_hash():
    """Verify that the hash produced by the agent matches the baseline."""
    baseline_path = "/home/user/baseline.py"
    frames_dir = "/home/user/frames"
    baseline_out = "/home/user/baseline_out.txt"
    agent_out = "/home/user/audit_trail.txt"

    assert os.path.isfile(agent_out), f"Agent output file {agent_out} is missing."

    # Run baseline to get the expected hash
    subprocess.run(["python3", baseline_path, frames_dir, baseline_out], check=True)

    with open(baseline_out, "r") as f:
        expected_hash = f.read().strip()

    with open(agent_out, "r") as f:
        agent_hash = f.read().strip()

    assert expected_hash == agent_hash, f"Hash mismatch! Expected {expected_hash}, got {agent_hash}"

def test_performance_speedup():
    """Verify that the C++ hasher meets the performance threshold."""
    baseline_path = "/home/user/baseline.py"
    hasher_path = "/home/user/hasher"
    frames_dir = "/home/user/frames"

    assert os.path.isfile(hasher_path), f"Compiled C++ hasher {hasher_path} is missing."
    assert os.access(hasher_path, os.X_OK), f"Compiled C++ hasher {hasher_path} is not executable."

    # Warm up system caches to reduce I/O variance
    subprocess.run(["python3", baseline_path, frames_dir, "/dev/null"], check=True)
    subprocess.run([hasher_path, frames_dir, "/dev/null"], check=True)

    # Measure baseline Python script time
    t0 = time.time()
    subprocess.run(["python3", baseline_path, frames_dir, "/dev/null"], check=True)
    baseline_time = time.time() - t0

    # Measure agent C++ hasher time
    t0 = time.time()
    subprocess.run([hasher_path, frames_dir, "/dev/null"], check=True)
    agent_time = time.time() - t0

    # C++ program might be extremely fast, prevent division by zero
    if agent_time <= 0:
        agent_time = 1e-9

    speedup = baseline_time / agent_time
    assert speedup >= 2.0, f"Speedup is {speedup:.2f}x, which is below the required 2.0x threshold (Baseline: {baseline_time:.4f}s, Agent: {agent_time:.4f}s)."