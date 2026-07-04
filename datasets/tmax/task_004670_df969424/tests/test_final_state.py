# test_final_state.py
import os
import pytest
import csv

def test_generate_py_updated():
    generate_py = "/home/user/ml_data/generate.py"
    assert os.path.isfile(generate_py), f"File missing: {generate_py}"

    with open(generate_py, 'r') as f:
        content = f.read()

    assert "solve_ivp" in content, "generate.py does not use scipy.integrate.solve_ivp"
    assert "BDF" in content or "Radau" in content or "LSODA" in content, "generate.py does not seem to specify a stiff solver method like BDF or Radau"

def test_calc_stats_compiled():
    calc_stats = "/home/user/ml_data/stats_tool/calc_stats"
    assert os.path.isfile(calc_stats), f"Executable missing: {calc_stats}"
    assert os.access(calc_stats, os.X_OK), f"File is not executable: {calc_stats}"

def test_dataset_csv_valid():
    dataset_csv = "/home/user/ml_data/dataset.csv"
    assert os.path.isfile(dataset_csv), f"File missing: {dataset_csv}"

    with open(dataset_csv, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, "dataset.csv is empty"

        for row_idx, row in enumerate(reader, start=2):
            for col_idx, val in enumerate(row):
                val_upper = val.strip().upper()
                assert "NAN" not in val_upper and "INF" not in val_upper, \
                    f"dataset.csv contains invalid value '{val}' at row {row_idx}, col {col_idx}"

def test_stability_report():
    report_txt = "/home/user/ml_data/stability_report.txt"
    assert os.path.isfile(report_txt), f"File missing: {report_txt}"

    with open(report_txt, 'r') as f:
        content = f.read().strip()

    assert content != "NaN_or_Inf", "stability_report.txt indicates NaNs or Infs were found by the stats tool"

    try:
        max_val = float(content)
    except ValueError:
        pytest.fail(f"stability_report.txt does not contain a valid float: '{content}'")

    assert 2.0 <= max_val <= 2.05, f"Maximum amplitude {max_val} in stability_report.txt is not within the expected range [2.0, 2.05] for the stable limit cycle"