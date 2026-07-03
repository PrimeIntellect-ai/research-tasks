# test_final_state.py
import os
import csv

def test_rust_project_exists():
    cargo_toml_path = "/home/user/config_tracker/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"Rust project Cargo.toml not found at {cargo_toml_path}. Did you create the cargo project?"

def test_output_csv_exists_and_correct():
    output_path = "/home/user/output/config_summary.csv"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    expected_rows = [
        ["normalized_key", "num_changes", "first_value", "latest_value"],
        ["db_host", "1", "localhost", "127.0.0.1"],
        ["enable_cache", "1", "true", "false"],
        ["log_level", "2", "INFO", "WARN"],
        ["max_connections", "1", "100", "150"],
        ["server_port", "1", "8080", "8081"],
        ["timeout", "0", "30", "30"]
    ]

    actual_rows = []
    with open(output_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) > 0, f"Output file {output_path} is empty."

    # Check headers
    assert actual_rows[0] == expected_rows[0], f"Headers mismatch in {output_path}. Expected {expected_rows[0]}, got {actual_rows[0]}"

    # Check data rows
    assert actual_rows == expected_rows, f"Data mismatch in {output_path}. Expected {expected_rows}, got {actual_rows}"