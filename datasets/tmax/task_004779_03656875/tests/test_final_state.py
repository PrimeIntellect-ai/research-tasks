# test_final_state.py
import os
import re

def test_run_workflow_sh():
    path = "/home/user/run_workflow.sh"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_fit_params_txt():
    path = "/home/user/fit_params.txt"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    match = re.search(r"A=([0-9.]+),\s*k=([0-9.]+)", content)
    assert match is not None, f"Could not parse A and k from {path}. Content was: {content}"

    A = float(match.group(1))
    k = float(match.group(2))

    # Ground truth values are roughly A=5.0, k=0.2
    assert 4.8 <= A <= 5.2, f"Value of A ({A}) is too far from expected 5.0"
    assert 0.15 <= k <= 0.25, f"Value of k ({k}) is too far from expected 0.2"

def test_integrated_data_csv():
    path = "/home/user/integrated_data.csv"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, "r") as f:
        header = f.readline().strip()

    assert header == "Time,Cumulative_C,Fitted_C", f"Incorrect header in {path}. Got: {header}"

def test_result_plot_png():
    path = "/home/user/result_plot.png"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, "rb") as f:
        magic_bytes = f.read(8)

    assert magic_bytes == b"\x89PNG\r\n\x1a\n", f"{path} is not a valid PNG file."