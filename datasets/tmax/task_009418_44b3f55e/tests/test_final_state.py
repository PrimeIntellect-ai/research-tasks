# test_final_state.py

import os
import pytest

def test_summary_txt_correctness():
    summary_file = "/home/user/log_pipeline/summary.txt"
    assert os.path.isfile(summary_file), f"{summary_file} does not exist. Did the pipeline run successfully?"

    with open(summary_file, "r") as f:
        content = f.read()

    assert "Records Processed: 3" in content, "summary.txt does not indicate that 3 records were processed. Concurrency or parsing issues may remain."
    assert "Total Bytes: 2300100000" in content, "summary.txt does not show the correct Total Bytes (2300100000). The C program may still have integer overflow, or DOS newlines were not handled properly."

def test_resolution_report_txt_correctness():
    report_file = "/home/user/log_pipeline/resolution_report.txt"
    assert os.path.isfile(report_file), f"{report_file} does not exist. You must create the resolution report."

    with open(report_file, "r") as f:
        first_line = f.readline().strip()

    assert first_line == "2300100000", f"The first line of resolution_report.txt must be strictly '2300100000', but found '{first_line}'."

def test_output_txt_no_race_conditions():
    output_file = "/home/user/log_pipeline/output.txt"
    assert os.path.isfile(output_file), f"{output_file} does not exist."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"output.txt should contain exactly 3 valid lines, found {len(lines)}. Race conditions or parsing errors might be dropping or duplicating data."

    for i, line in enumerate(lines):
        parts = line.split(",")
        assert len(parts) == 3, f"Line {i+1} in output.txt is malformed due to interleaved writes (race condition not fixed): '{line}'"

        # Ensure no trailing carriage returns remain
        assert not parts[-1].endswith("\r"), f"Line {i+1} in output.txt still contains DOS carriage returns: '{line}'"