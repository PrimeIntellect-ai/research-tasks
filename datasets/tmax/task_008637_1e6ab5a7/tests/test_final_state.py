# test_final_state.py

import os
import pytest

WORKSPACE_DIR = "/home/user/workspace"

def test_summary_txt_exists_and_correct():
    summary_path = os.path.join(WORKSPACE_DIR, "summary.txt")
    assert os.path.isfile(summary_path), f"File {summary_path} is missing."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    assert content == "3.7", f"Expected summary.txt to contain exactly '3.7', but found '{content}'"

def test_output_csv_correct():
    output_path = os.path.join(WORKSPACE_DIR, "output.csv")
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected output.csv to have 5 rows, but found {len(lines)}."

    first_col_sum = 0.0
    for i, line in enumerate(lines):
        parts = line.split(",")
        assert len(parts) == 2, f"Expected 2 columns in output.csv at row {i+1}, found {len(parts)}."

        val1 = float(parts[0])
        val2 = float(parts[1])

        assert val1 != 0.0 or val2 != 0.0, f"Row {i+1} still contains zeros. The pipeline might not have been recompiled or run correctly."
        first_col_sum += val1

    avg = first_col_sum / len(lines)
    assert round(avg, 1) == 3.7, f"Expected the average of the first column to be 3.7, but calculated {avg:.2f}."

def test_makefile_fixed():
    makefile_path = os.path.join(WORKSPACE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "USE_FAST_MATH" in content, "The Makefile does not appear to have been modified to include the USE_FAST_MATH macro."