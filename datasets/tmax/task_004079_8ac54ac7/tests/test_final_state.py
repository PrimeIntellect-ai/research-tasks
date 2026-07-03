# test_final_state.py

import os
import subprocess
import datetime
import pytest

def test_processor_patched():
    """Test that processor.c has been successfully patched."""
    src_file = "/home/user/src/processor.c"
    assert os.path.isfile(src_file), f"Source file {src_file} does not exist."
    with open(src_file, "r") as f:
        content = f.read()
    assert "char uid[256];" in content, "Source file does not appear to be patched with the new schema variables."
    assert "MINIMAL_CONTAINER" in content, "Source file does not appear to be patched with MINIMAL_CONTAINER logic."

def test_binary_compiled_statically():
    """Test that the binary is compiled and statically linked."""
    bin_file = "/home/user/bin/processor"
    assert os.path.isfile(bin_file), f"Binary {bin_file} does not exist."
    assert os.access(bin_file, os.X_OK), f"Binary {bin_file} is not executable."

    # Check if statically linked using 'file' command
    result = subprocess.run(["file", bin_file], capture_output=True, text=True)
    assert "statically linked" in result.stdout.lower(), f"Binary {bin_file} is not statically linked. 'file' output: {result.stdout}"

def test_data_migrated_correctly():
    """Test that the data was migrated correctly to the new schema."""
    old_file = "/home/user/data/old_events.tsv"
    new_file = "/home/user/data/new_events.tsv"

    assert os.path.isfile(old_file), f"Original data file {old_file} is missing."
    assert os.path.isfile(new_file), f"Migrated data file {new_file} does not exist."

    with open(old_file, "r") as f:
        old_lines = f.read().strip().split("\n")

    with open(new_file, "r") as f:
        new_lines = f.read().strip().split("\n")

    assert len(old_lines) == len(new_lines), "Migrated data file does not have the same number of lines as the original."

    for old_line, new_line in zip(old_lines, new_lines):
        if not old_line.strip():
            continue

        old_parts = old_line.split("\t")
        new_parts = new_line.split("\t")

        assert len(new_parts) == 3, f"Migrated line does not have 3 columns: {new_line}"

        expected_uid = f"U-{old_parts[0]}"
        assert new_parts[0] == expected_uid, f"Expected uid {expected_uid}, got {new_parts[0]}"

        expected_time = datetime.datetime.fromtimestamp(int(old_parts[1]), tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        assert new_parts[1] == expected_time, f"Expected time {expected_time}, got {new_parts[1]}"

        assert new_parts[2] == old_parts[2], f"Expected action {old_parts[2]}, got {new_parts[2]}"

def test_summary_output():
    """Test that the summary output is correct, indicating proper macro usage and processing."""
    out_file = "/home/user/output/summary.txt"
    assert os.path.isfile(out_file), f"Output file {out_file} does not exist."

    with open(out_file, "r") as f:
        content = f.read().strip()

    # Recompute expected values based on the data
    old_file = "/home/user/data/old_events.tsv"
    total = 0
    logins = 0
    if os.path.isfile(old_file):
        with open(old_file, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                total += 1
                if line.strip().endswith("\tlogin"):
                    logins += 1

    expected_output = f"MINIMAL_STAT: {total} total, {logins} logins"
    assert content == expected_output, f"Output file content '{content}' does not match expected '{expected_output}'. This checks both processing logic and the -DMINIMAL_CONTAINER compilation flag."