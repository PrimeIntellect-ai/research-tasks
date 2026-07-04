# test_final_state.py

import os
import csv
import ast
import pytest

def test_script_exists_and_uses_parallelism():
    """Verify the script exists and uses a parallel processing library."""
    script_path = "/home/user/process_configs.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"Script contains syntax errors: {e}")

    uses_parallel = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("multiprocessing") or alias.name.startswith("concurrent.futures"):
                    uses_parallel = True
        elif isinstance(node, ast.ImportFrom):
            if node.module and (node.module.startswith("multiprocessing") or node.module.startswith("concurrent.futures")):
                uses_parallel = True

    assert uses_parallel, "Script does not import 'multiprocessing' or 'concurrent.futures' for parallel processing."

def test_output_csv_correct():
    """Verify the generated CSV matches the expected normalized and aggregated format."""
    csv_path = "/home/user/normalized_configs.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Output CSV is empty."

    header = rows[0]
    expected_header = ["aligned_hour", "server_name", "param_name", "param_value"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}."

    data = rows[1:]

    expected_data = [
        ("2023-05-10 08:00:00", "db01", "timeout", 60.0),
        ("2023-05-10 08:00:00", "db01", "workers", 8.0),
        ("2023-05-10 08:00:00", "web01", "timeout", 30.0),
        ("2023-05-10 08:00:00", "web01", "workers", 5.0),
        ("2023-05-10 09:00:00", "db01", "workers", 8.0),
        ("2023-05-10 09:00:00", "web01", "timeout", 45.0),
        ("2023-05-10 09:00:00", "web01", "workers", 5.0),
        ("2023-05-11 14:00:00", "db01", "timeout", 120.0),
        ("2023-05-11 14:00:00", "db01", "workers", 16.0),
        ("2023-05-11 14:00:00", "web01", "timeout", 60.0),
        ("2023-05-11 14:00:00", "web01", "workers", 8.0),
        ("2023-05-11 15:00:00", "db01", "timeout", 120.0),
        ("2023-05-11 15:00:00", "db01", "workers", 32.0),
        ("2023-05-11 15:00:00", "web01", "timeout", 60.0),
        ("2023-05-11 15:00:00", "web01", "workers", 8.0)
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} data rows, got {len(data)}."

    for i, (row, exp) in enumerate(zip(data, expected_data)):
        assert len(row) == 4, f"Row {i+1} does not have exactly 4 columns: {row}"
        assert row[0] == exp[0], f"Row {i+1} aligned_hour mismatch: expected '{exp[0]}', got '{row[0]}'"
        assert row[1] == exp[1], f"Row {i+1} server_name mismatch: expected '{exp[1]}', got '{row[1]}'"
        assert row[2] == exp[2], f"Row {i+1} param_name mismatch: expected '{exp[2]}', got '{row[2]}'"

        try:
            val = float(row[3])
        except ValueError:
            pytest.fail(f"Row {i+1} param_value is not a valid number: '{row[3]}'")

        assert val == exp[3], f"Row {i+1} param_value mismatch: expected {exp[3]}, got {val}"