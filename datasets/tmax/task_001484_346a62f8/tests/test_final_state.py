# test_final_state.py

import os
import csv
import subprocess
import pytest

def test_process_script_exists_and_runs():
    script_path = "/home/user/process.py"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    # Run the script
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to run. Stderr: {result.stderr}"

def test_summary_csv():
    summary_path = "/home/user/summary.csv"
    assert os.path.isfile(summary_path), f"Summary CSV not found at {summary_path}"

    with open(summary_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Summary CSV is empty"

    header = rows[0]
    assert header == ["category", "mean_pred"], f"Unexpected header: {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 4, f"Expected 4 categories, found {len(data_rows)}"

    categories = set()
    for row in data_rows:
        assert len(row) == 2, f"Expected 2 columns in row, got {len(row)}"
        categories.add(row[0])
        try:
            float(row[1])
        except ValueError:
            pytest.fail(f"mean_pred value '{row[1]}' is not a valid float")

    assert categories == {"A", "B", "C", "D"}, f"Unexpected categories: {categories}"

def test_plot_png():
    plot_path = "/home/user/plot.png"
    assert os.path.isfile(plot_path), f"Plot image not found at {plot_path}"
    assert os.path.getsize(plot_path) > 0, "Plot image is empty (0 bytes)"