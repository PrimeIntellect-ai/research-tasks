# test_final_state.py
import os
import pytest

def test_main_rs_restored():
    main_rs_path = "/home/user/telemetry_app/src/main.rs"
    assert os.path.isfile(main_rs_path), f"The source code file {main_rs_path} was not restored."

def test_corrected_metrics_output():
    output_file = "/home/user/telemetry_app/corrected_metrics.txt"
    assert os.path.isfile(output_file), f"The output file {output_file} was not generated."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "4125000000",
        "4125000000",
        "3750000000",
        "3925000000",
        "5050000000",
        "6150000000"
    ]

    assert len(lines) == len(expected), f"Expected {len(expected)} lines in {output_file}, but got {len(lines)}."

    for i, (actual, exp) in enumerate(zip(lines, expected)):
        assert actual == exp, f"Line {i+1} in {output_file} is incorrect. Expected {exp}, got {actual}."