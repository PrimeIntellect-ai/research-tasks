# test_final_state.py
import os
import csv
import json

def compute_expected_values():
    data_path = "/home/user/data.csv"
    if not os.path.exists(data_path):
        return 0, 0, 0.0

    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        data = [[float(x) for x in row] for row in reader if row]

    rows = len(data)
    cols = len(data[0]) if rows > 0 else 0

    if rows <= 1:
        return rows, cols, 0.0

    trace = 0.0
    for c in range(cols):
        col_data = [data[r][c] for r in range(rows)]
        mean = sum(col_data) / rows
        variance = sum((x - mean) ** 2 for x in col_data) / (rows - 1)
        trace += variance

    return rows, cols, round(trace, 4)

def test_pca_prep_exists():
    """Check if the Rust project directory exists."""
    assert os.path.isdir("/home/user/pca_prep"), "Rust project directory /home/user/pca_prep is missing."

def test_experiment_log_exists():
    """Check if the output JSON file exists."""
    assert os.path.isfile("/home/user/experiment_log.json"), "Output file /home/user/experiment_log.json is missing."

def test_experiment_log_content():
    """Validate the contents of the experiment log JSON."""
    log_path = "/home/user/experiment_log.json"

    try:
        with open(log_path, 'r') as f:
            result = json.load(f)
    except Exception as e:
        assert False, f"Failed to read or parse /home/user/experiment_log.json: {e}"

    expected_rows, expected_cols, expected_variance = compute_expected_values()

    assert "rows" in result, "'rows' key missing in JSON output."
    assert "cols" in result, "'cols' key missing in JSON output."
    assert "total_variance" in result, "'total_variance' key missing in JSON output."

    assert result["rows"] == expected_rows, f"Expected {expected_rows} rows, got {result['rows']}."
    assert result["cols"] == expected_cols, f"Expected {expected_cols} cols, got {result['cols']}."

    agent_variance = result["total_variance"]
    assert isinstance(agent_variance, (int, float)), "total_variance must be a number."

    # Allow small floating point differences due to rounding
    diff = abs(float(agent_variance) - expected_variance)
    assert diff <= 0.0001, f"Expected total_variance {expected_variance}, got {agent_variance}."