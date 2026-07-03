# test_final_state.py

import os
import csv
import pytest

def test_circular_dependency_fixed():
    """Verify that the circular inclusion dependency has been resolved."""
    base_dir = "/home/user/log_processor"
    parser_h = os.path.join(base_dir, "parser.h")
    validator_h = os.path.join(base_dir, "validator.h")

    assert os.path.isfile(parser_h), f"Missing {parser_h}"
    assert os.path.isfile(validator_h), f"Missing {validator_h}"

    with open(parser_h, "r") as f:
        p_content = f.read()
    with open(validator_h, "r") as f:
        v_content = f.read()

    p_includes_v = '#include "validator.h"' in p_content
    v_includes_p = '#include "parser.h"' in v_content

    assert not (p_includes_v and v_includes_p), (
        "Circular dependency still exists: parser.h and validator.h mutually include each other. "
        "Use forward declarations to break the cycle."
    )

def test_executable_exists():
    """Verify that the project was successfully compiled."""
    executable = "/home/user/log_processor/processor"
    assert os.path.isfile(executable), f"Executable {executable} not found. Did you run 'make'?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_processed_csv_output():
    """Verify that the output CSV matches the expected logic for checksums and rate limits."""
    output_file = "/home/user/processed.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} not found. Did you run the processor?"

    # Expected statuses based on the rules applied to requests.csv
    expected_statuses = [
        "OK",                # 1600000000.1,userA,010203,00 -> valid, 0 prev
        "OK",                # 1600000000.2,userA,010203,00 -> valid, 1 prev
        "OK",                # 1600000000.3,userA,ff01,fe   -> valid, 2 prev
        "RATE_LIMITED",      # 1600000000.4,userA,1020,30   -> valid, 3 prev (0.1, 0.2, 0.3)
        "RATE_LIMITED",      # 1600000000.5,userA,1020,30   -> valid, 4 prev
        "OK",                # 1600000000.6,userB,01,01     -> valid, 0 prev
        "INVALID_CHECKSUM",  # 1600000000.7,userB,01,02     -> invalid checksum
        "RATE_LIMITED"       # 1600000001.2,userA,01,01     -> valid, 3 prev in (0.2, 1.2] (0.3, 0.4, 0.5)
    ]

    with open(output_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == len(expected_statuses), (
        f"Expected {len(expected_statuses)} rows in output, but found {len(rows)}."
    )

    for i, (row, expected_status) in enumerate(zip(rows, expected_statuses)):
        assert len(row) >= 5, f"Row {i+1} does not have the expected 5 columns."
        actual_status = row[4].strip()
        assert actual_status == expected_status, (
            f"Row {i+1}: expected status '{expected_status}', but got '{actual_status}'."
        )