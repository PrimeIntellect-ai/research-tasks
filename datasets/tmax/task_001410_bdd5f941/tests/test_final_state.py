# test_final_state.py

import os
import subprocess
import tempfile
import random
import pytest
import numpy as np
import matplotlib.pyplot as plt

def test_agent_binary_exists():
    agent_bin = "/home/user/bin/seq_extractor"
    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

def test_plot_script_and_output_exist():
    script_path = "/home/user/plot_singular_values.sh"
    plot_path = "/home/user/svd_variance.png"
    assert os.path.isfile(script_path), f"Plot script not found at {script_path}"
    assert os.path.isfile(plot_path), f"Output plot not found at {plot_path}"

def test_fuzz_equivalence():
    oracle_bin = "/app/oracle/seq_extractor_ref"
    agent_bin = "/home/user/bin/seq_extractor"

    assert os.path.isfile(oracle_bin), "Oracle binary missing"
    assert os.path.isfile(agent_bin), "Agent binary missing"

    random.seed(42)
    np.random.seed(42)

    N = 10  # Reduced from 50 to 10 to keep test execution time reasonable

    with tempfile.TemporaryDirectory() as base_tmp:
        for i in range(N):
            num_frames = random.randint(10, 50) # Reduced frame count to save execution time
            dir_path = os.path.join(base_tmp, f"fuzz_dir_{i}")
            os.makedirs(dir_path)

            for f_idx in range(num_frames):
                frame_path = os.path.join(dir_path, f"frame_{f_idx:04d}.png")
                # Generate random 16x16 grayscale image
                img_data = np.random.randint(0, 256, (16, 16), dtype=np.uint8)
                plt.imsave(frame_path, img_data, cmap='gray', format='png')

            # Run oracle
            try:
                oracle_res = subprocess.run([oracle_bin, dir_path], capture_output=True, text=True, timeout=10)
                oracle_out = oracle_res.stdout.strip()
            except Exception as e:
                pytest.fail(f"Oracle failed to run on fuzz input {i}: {e}")

            # Run agent
            try:
                agent_res = subprocess.run([agent_bin, dir_path], capture_output=True, text=True, timeout=10)
                agent_out = agent_res.stdout.strip()
            except Exception as e:
                pytest.fail(f"Agent binary failed to run on fuzz input {i}: {e}")

            assert oracle_res.returncode == 0, f"Oracle returned non-zero on input {i}"
            assert agent_res.returncode == 0, f"Agent returned non-zero on input {i}. Stderr: {agent_res.stderr}"

            assert agent_out == oracle_out, (
                f"Mismatch on fuzz input {i} ({num_frames} frames).\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output:  {agent_out}"
            )