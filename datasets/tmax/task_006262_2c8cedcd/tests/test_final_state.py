# test_final_state.py

import os
import csv
import pytest

def test_rust_project_exists():
    """Verify that the Rust Cargo project was created in the correct location."""
    cargo_toml = "/home/user/config_tracker/Cargo.toml"
    main_rs = "/home/user/config_tracker/src/main.rs"

    assert os.path.exists(cargo_toml), f"Cargo.toml not found at {cargo_toml}. Did you create the Cargo project?"
    assert os.path.exists(main_rs), f"main.rs not found at {main_rs}. Did you create the Cargo project?"

def test_latest_state_csv_exists():
    """Verify that the output CSV file was created."""
    output_csv = "/home/user/latest_state.csv"
    assert os.path.exists(output_csv), f"Output file {output_csv} is missing."
    assert os.path.isfile(output_csv), f"Path {output_csv} is not a regular file."

def test_latest_state_csv_content():
    """Verify that the output CSV contains the correct aggregated state, headers, and sorting."""
    output_csv = "/home/user/latest_state.csv"

    # We expect the file to be readable as UTF-8
    try:
        with open(output_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
    except UnicodeDecodeError:
        pytest.fail("The output CSV is not valid UTF-8.")

    assert len(rows) > 0, "The output CSV is empty."

    # Check header
    expected_header = ["config_key", "server_name", "decoded_value"]
    assert rows[0] == expected_header, f"Expected header {expected_header}, but got {rows[0]}"

    # Check data rows
    expected_data = [
        ["db_timeout", "srv-alpha", "60s"],
        ["system_path", "srv-delta", "C:\\Windows\\System32"],
        ["timezone", "srv-beta", "Europe/Paris"],
        ["welcome_msg", "srv-gamma", "Maintenance …"],
    ]

    actual_data = rows[1:]

    assert actual_data == expected_data, (
        f"The data rows in the CSV do not match the expected output. "
        f"Expected:\n{expected_data}\nGot:\n{actual_data}"
    )