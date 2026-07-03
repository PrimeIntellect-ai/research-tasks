# test_final_state.py
import os
import math

def test_features_csv():
    features_csv = "/home/user/data/features.csv"
    assert os.path.isfile(features_csv), f"Output file {features_csv} does not exist."

    with open(features_csv, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 6, f"Expected 6 lines in {features_csv} (header + 5 rows), found {len(lines)}."

    expected_header = "timestamp,sensor_A,sensor_B,diff,magnitude"
    assert lines[0] == expected_header, f"Header mismatch. Expected '{expected_header}', got '{lines[0]}'."

    expected_rows = [
        "1600000000,10.0,5.0,5.0,11.1803",
        "1600000060,12.0,9.0,3.0,15.0000",
        "1600000120,8.0,15.0,-7.0,17.0000",
        "1600000180,-3.0,4.0,-7.0,5.0000",
        "1600000240,0.0,0.0,0.0,0.0000"
    ]

    for i, expected_row in enumerate(expected_rows):
        assert lines[i+1] == expected_row, f"Row {i+1} mismatch. Expected '{expected_row}', got '{lines[i+1]}'."

def test_experiments_txt():
    experiments_txt = "/home/user/experiments.txt"
    assert os.path.isfile(experiments_txt), f"Log file {experiments_txt} does not exist."

    with open(experiments_txt, "r") as f:
        content = f.read().strip()

    expected_log = "SUCCESS: Processed 5 rows."
    assert expected_log in content, f"Expected log '{expected_log}' not found in {experiments_txt}."

def test_rust_project_files():
    cargo_toml = "/home/user/sensor_pipeline/Cargo.toml"
    main_rs = "/home/user/sensor_pipeline/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project file {cargo_toml} does not exist."
    assert os.path.isfile(main_rs), f"Rust source file {main_rs} does not exist."