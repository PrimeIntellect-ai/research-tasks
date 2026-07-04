# test_final_state.py

import os
import re
import pytest

def test_fit_model_c_fixed():
    file_path = "/home/user/fit_model.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    # Check that dt = 0.01 is present
    assert "0.01" in content, "The step size dt was not changed to 0.01 in fit_model.c."

    # Ensure dt = 1.0 is no longer assigned to dt
    # A simple check:
    matches = re.findall(r'dt\s*=\s*1\.0\s*;', content)
    assert len(matches) == 0, "The incorrect step size dt = 1.0 is still present in fit_model.c."

def test_fit_model_compiled():
    file_path = "/home/user/fit_model"
    assert os.path.isfile(file_path), f"Compiled binary {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_optimal_k_output():
    file_path = "/home/user/optimal_k.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    try:
        k_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse {content} as a float in {file_path}.")

    assert abs(k_val - 0.5255) < 0.01, f"Expected optimal k to be around 0.5255, but got {k_val}."

def test_plot_gp():
    file_path = "/home/user/plot.gp"
    assert os.path.isfile(file_path), f"Gnuplot script {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().lower()

    assert "set terminal png" in content or "set term png" in content, "The gnuplot script does not set the terminal to png."
    assert "set output" in content and "plot.png" in content, "The gnuplot script does not set the output to plot.png."
    assert "plot" in content and "data.csv" in content, "The gnuplot script does not plot the data.csv file."