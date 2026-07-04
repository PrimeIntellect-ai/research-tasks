# test_final_state.py

import os
import subprocess
import random
import pytest

def test_video_features_csv_exists_and_format():
    """Test that the video features CSV was generated with the correct headers and some data."""
    csv_path = "/home/user/video_features.csv"
    assert os.path.exists(csv_path), f"Missing required file: {csv_path}"

    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 1, f"CSV {csv_path} has no data lines."
    assert lines[0].strip() == "frame,R_avg,G_avg,B_avg", f"Incorrect headers in {csv_path}. Expected 'frame,R_avg,G_avg,B_avg', got '{lines[0]}'"

    # Check that subsequent lines have 4 comma-separated values
    for i, line in enumerate(lines[1:], start=2):
        parts = line.split(',')
        assert len(parts) == 4, f"Line {i} in {csv_path} does not have exactly 4 columns: {line}"

def test_rolling_cov_fuzz_equivalence():
    """Fuzz test the student's rolling covariance binary against the reference oracle."""
    agent_bin = "/home/user/rolling_cov"
    ref_bin = "/app/ref_rolling_cov"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary is not executable: {agent_bin}"
    assert os.path.exists(ref_bin), f"Reference binary not found at {ref_bin}"

    random.seed(42)
    N_RUNS = 1000

    for i in range(N_RUNS):
        W = random.randint(2, 100)
        L = random.randint(W, W + 500)

        input_lines = [str(W)]
        for _ in range(L):
            r = random.uniform(0.0, 255.0)
            g = random.uniform(0.0, 255.0)
            b = random.uniform(0.0, 255.0)
            input_lines.append(f"{r:.6f},{g:.6f},{b:.6f}")

        input_data = "\n".join(input_lines) + "\n"

        ref_proc = subprocess.run(
            [ref_bin], 
            input=input_data, 
            text=True, 
            capture_output=True
        )
        agent_proc = subprocess.run(
            [agent_bin], 
            input=input_data, 
            text=True, 
            capture_output=True
        )

        assert ref_proc.returncode == 0, f"Reference binary failed on run {i}"
        assert agent_proc.returncode == 0, f"Agent binary failed on run {i} with error: {agent_proc.stderr}"

        if agent_proc.stdout != ref_proc.stdout:
            # Truncate outputs for display if they are too long
            ref_out = ref_proc.stdout
            agent_out = agent_proc.stdout
            if len(ref_out) > 500:
                ref_out = ref_out[:500] + "\n...[truncated]"
            if len(agent_out) > 500:
                agent_out = agent_out[:500] + "\n...[truncated]"

            pytest.fail(
                f"Mismatch on fuzz run {i}.\n"
                f"Input parameters: W={W}, L={L}\n"
                f"--- Reference Output (first 500 chars) ---\n{ref_out}\n"
                f"--- Agent Output (first 500 chars) ---\n{agent_out}\n"
            )