# test_final_state.py

import os
import math
import pytest

def test_venv_exists():
    """Check that the Python virtual environment was created at the correct location."""
    venv_python = "/home/user/sim_env/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment Python executable not found at {venv_python}."

def test_script_exists():
    """Check that the analysis script exists."""
    script_path = "/home/user/analyze_mesh.py"
    assert os.path.isfile(script_path), f"Analysis script not found at {script_path}."

def test_total_volume():
    """Check that the total volume of refined cells is calculated correctly."""
    data_path = "/home/user/mesh_data.csv"
    assert os.path.isfile(data_path), f"Data file {data_path} is missing."

    # Recompute the expected total volume from the actual data file
    refined_vols = []
    with open(data_path, 'r') as f:
        header = f.readline()
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) >= 2:
                vol = float(parts[1])
                if vol < 0.05:
                    refined_vols.append(vol)

    expected_total_vol = math.fsum(refined_vols)
    expected_str = f"{expected_total_vol:.8f}"

    output_path = "/home/user/total_volume.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Expected total volume {expected_str}, but got {actual_str}."

def test_bootstrap_ci():
    """Check that the bootstrap confidence interval is calculated correctly."""
    output_path = "/home/user/bootstrap_ci.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        actual_str = f.read().strip()

    # The expected string is deterministic based on the fixed seed generation and parameters
    expected_str = "0.02462319,0.02542472"

    assert actual_str == expected_str, f"Expected bootstrap CI {expected_str}, but got {actual_str}."