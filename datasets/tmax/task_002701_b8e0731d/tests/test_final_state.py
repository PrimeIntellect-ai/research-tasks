# test_final_state.py

import os
import re
import pytest

def test_integrator_fixed():
    integrator_path = "/home/user/sim_engine/src/integrator.rs"
    assert os.path.isfile(integrator_path), f"{integrator_path} does not exist."

    with open(integrator_path, "r") as f:
        content = f.read()

    # The bug was `let scale = error / tolerance;`
    # The fix should invert this logic, typically `let scale = tolerance / error;`
    assert "error / tolerance" not in content, "The bug 'error / tolerance' is still present in integrator.rs."
    assert "tolerance / error" in content, "The fix 'tolerance / error' was not found in integrator.rs."

def test_sim_output_valid():
    output_path = "/home/user/sim_output.csv"
    assert os.path.isfile(output_path), f"{output_path} was not created."

    with open(output_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 1, f"{output_path} does not contain enough data."
    assert "time,node1_x,node1_v" in lines[0], f"{output_path} header is incorrect."

    for line in lines[1:]:
        assert "NaN" not in line, f"NaN found in simulation output: {line}"
        parts = line.split(',')
        assert len(parts) == 3, f"Invalid row format in {output_path}: {line}"
        try:
            [float(p) for p in parts]
        except ValueError:
            pytest.fail(f"Non-numeric data found in {output_path}: {line}")

def test_evaluation_log():
    log_path = "/home/user/evaluation.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    match = re.search(r"MSE:\s*([0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)", content)
    assert match is not None, f"Could not find 'MSE: <value>' in {log_path}. Content: {content}"

    mse_value = float(match.group(1))
    assert mse_value >= 0, f"MSE value cannot be negative, got {mse_value}."
    assert mse_value < 0.1, f"MSE value is suspiciously high ({mse_value}), indicating the simulation might still be diverging or incorrect."

def test_plot_artifacts_exist():
    script_path = "/home/user/plot_data.py"
    plot_path = "/home/user/trajectory_plot.svg"

    assert os.path.isfile(script_path), f"Plotting script {script_path} does not exist."
    assert os.path.isfile(plot_path), f"Plot image {plot_path} does not exist."

    # Basic check to ensure it's an SVG file
    with open(plot_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    assert "<svg" in content.lower(), f"{plot_path} does not appear to be a valid SVG file."