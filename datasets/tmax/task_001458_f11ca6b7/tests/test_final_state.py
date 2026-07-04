# test_final_state.py
import os
import csv

def test_venv_exists():
    """Verify that the virtual environment python executable exists."""
    python_path = '/home/user/scipy_env/bin/python'
    assert os.path.exists(python_path), f"Virtual environment python not found at {python_path}"
    assert os.access(python_path, os.X_OK), f"Python executable at {python_path} is not executable"

def test_quad_result():
    """Verify that the quad result file exists and contains a valid float."""
    result_path = '/home/user/quad_result.txt'
    assert os.path.exists(result_path), f"File not found: {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {result_path} is not a valid float: '{content}'"

    # The integral of sin(100x)*exp(-x) from 0 to 5 is approximately 0.010058
    # The truth code mentions 0.009999, so we allow a reasonable range.
    assert 0.009 < val < 0.011, f"Computed integral {val} is far from the expected value (~0.010)"

def test_mc_convergence_csv():
    """Verify the Monte Carlo convergence CSV file structure and contents."""
    csv_path = '/home/user/mc_convergence.csv'
    assert os.path.exists(csv_path), f"File not found: {csv_path}"

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty"
    assert rows[0] == ["N", "Estimate", "Error"], f"Incorrect CSV header: {rows[0]}"

    expected_Ns = ["10000", "50000", "100000", "500000"]
    actual_Ns = []

    for i, row in enumerate(rows[1:], start=1):
        assert len(row) == 3, f"Row {i} does not have exactly 3 columns: {row}"
        actual_Ns.append(row[0])
        try:
            float(row[1])
            float(row[2])
        except ValueError:
            assert False, f"Estimate or Error in row {i} is not a valid float: {row}"

    assert actual_Ns == expected_Ns, f"Expected N values {expected_Ns}, but got {actual_Ns}"

def test_convergence_plot():
    """Verify that the convergence plot was generated."""
    plot_path = '/home/user/convergence.png'
    assert os.path.exists(plot_path), f"Plot file not found: {plot_path}"
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty"