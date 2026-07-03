# test_final_state.py

import os
import re
import pytest

def test_simulate_c_exists():
    """Verify that the C program was created."""
    path = "/home/user/simulate.c"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_plot_png_exists():
    """Verify that the gnuplot output image was created."""
    path = "/home/user/plot.png"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_sim_data_csv_exists():
    """Verify that the simulation data CSV was created."""
    path = "/home/user/sim_data.csv"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_results_txt_content():
    """Verify the contents of results.txt match the expected MSE and Best hypothesis."""
    path = "/home/user/results.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check MSE_H1
    match_h1 = re.search(r"MSE_H1:\s*(0\.00305[7-9])", content)
    assert match_h1 is not None, f"Could not find matching MSE_H1 (expected ~0.003058) in {path}. Content:\n{content}"

    # Check MSE_H2
    match_h2 = re.search(r"MSE_H2:\s*(0\.00003[0-1])", content)
    assert match_h2 is not None, f"Could not find matching MSE_H2 (expected ~0.000030) in {path}. Content:\n{content}"

    # Check Best
    match_best = re.search(r"Best:\s*H2", content)
    assert match_best is not None, f"Could not find 'Best: H2' in {path}. Content:\n{content}"