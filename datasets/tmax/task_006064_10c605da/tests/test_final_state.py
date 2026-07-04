# test_final_state.py
import os
import pytest

def test_rust_bug_fixed():
    main_rs = "/home/user/nlp_tools/src/main.rs"
    assert os.path.isfile(main_rs), f"main.rs is missing at {main_rs}."

    with open(main_rs, "r") as f:
        content = f.read()

    # The bug should be fixed, so it shouldn't just keep non-alphabetic characters.
    assert ".filter(|c| !c.is_alphabetic())" not in content, "The bug in main.rs was not fixed. It still filters out alphabetic characters."
    # We expect it to keep alphabetic and whitespace characters
    assert "is_alphabetic" in content, "The filter condition should still use is_alphabetic to keep letters."

def test_top_tokens_output():
    top_tokens_path = "/home/user/output/top_tokens.txt"
    assert os.path.isfile(top_tokens_path), f"Output file missing at {top_tokens_path}"

    with open(top_tokens_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_tokens = ["the", "quick", "dog"]
    assert lines == expected_tokens, f"Top tokens output is incorrect. Expected {expected_tokens}, got {lines}"

def test_covariance_matrix_output():
    cov_path = "/home/user/output/covariance.csv"
    assert os.path.isfile(cov_path), f"Output file missing at {cov_path}"

    with open(cov_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Covariance matrix should have 3 rows, got {len(lines)}"

    # Expected matrix values based on the sample covariance of the top 3 tokens
    expected_matrix = [
        ["1.8000", "0.1500", "0.0000"],
        ["0.1500", "0.2000", "0.0000"],
        ["0.0000", "0.0000", "0.5000"]
    ]

    for i, line in enumerate(lines):
        row = line.split(",")
        assert len(row) == 3, f"Row {i} of covariance matrix does not have 3 columns: {line}"
        for j, val in enumerate(row):
            expected_val = expected_matrix[i][j]
            # Allow slight floating point differences if they used different formatting, but it should match 4 decimal places
            assert val == expected_val, f"Mismatch in covariance matrix at row {i}, col {j}. Expected {expected_val}, got {val}"