# test_final_state.py

import os
import csv
import math

def test_params_csv_exists_and_valid():
    """Test that params.csv exists, has correct header, and valid parameters."""
    params_file = "/home/user/workspace/params.csv"
    assert os.path.isfile(params_file), f"File {params_file} is missing."

    with open(params_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) >= 2, f"{params_file} does not have enough rows."

    header = [h.strip() for h in rows[0]]
    assert header == ["shape", "scale"], f"Header in {params_file} is incorrect. Expected ['shape', 'scale'], got {header}."

    try:
        shape = float(rows[1][0])
        scale = float(rows[1][1])
    except ValueError:
        pytest.fail(f"Values in {params_file} are not valid floats: {rows[1]}")

    # Check approximate values based on truth
    assert math.isclose(shape, 2.5186, rel_tol=0.05), f"Shape parameter {shape} is out of expected range."
    assert math.isclose(scale, 1.4552, rel_tol=0.05), f"Scale parameter {scale} is out of expected range."

def test_ks_stat_txt_exists_and_valid():
    """Test that ks_stat.txt exists and contains the correct D statistic."""
    ks_file = "/home/user/workspace/ks_stat.txt"
    assert os.path.isfile(ks_file), f"File {ks_file} is missing."

    with open(ks_file, "r") as f:
        content = f.read().strip()

    try:
        ks_stat = float(content)
    except ValueError:
        pytest.fail(f"Content of {ks_file} is not a valid float: {content}")

    # Expected is approx 0.0163
    assert math.isclose(ks_stat, 0.0163, abs_tol=0.005), f"KS statistic {ks_stat} is out of expected range."

def test_cdf_plot_png_exists():
    """Test that cdf_plot.png exists and has a valid PNG signature."""
    plot_file = "/home/user/workspace/cdf_plot.png"
    assert os.path.isfile(plot_file), f"Plot file {plot_file} is missing."

    # Check PNG signature
    with open(plot_file, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"File {plot_file} is not a valid PNG file."

def test_scripts_exist():
    """Test that the requested scripts were created."""
    py_script = "/home/user/workspace/fit_model.py"
    r_script = "/home/user/workspace/validate.R"

    assert os.path.isfile(py_script), f"Python script {py_script} is missing."
    assert os.path.isfile(r_script), f"R script {r_script} is missing."