# test_final_state.py

import os
import glob
import pytest

def test_processed_files_exist():
    processed_dir = "/home/user/dataset_processed"

    assert os.path.isdir(processed_dir), f"Target directory missing: {processed_dir}"

    partA_expected = os.path.join(processed_dir, "partA_E7.gcode")
    partB_expected = os.path.join(processed_dir, "partB_E150.gcode")

    assert os.path.isfile(partA_expected), f"Expected file not found: {partA_expected}"
    assert os.path.isfile(partB_expected), f"Expected file not found: {partB_expected}"

    # Check that partC was skipped
    partC_files = glob.glob(os.path.join(processed_dir, "*partC*"))
    assert len(partC_files) == 0, f"Corrupted partC should have been skipped, but found: {partC_files}"

def test_processed_files_content():
    processed_dir = "/home/user/dataset_processed"
    partA_expected = os.path.join(processed_dir, "partA_E7.gcode")
    partB_expected = os.path.join(processed_dir, "partB_E150.gcode")

    with open(partA_expected, 'r') as f:
        contentA = f.read()
    assert "E7.8" in contentA, f"File {partA_expected} missing expected content 'E7.8'"
    assert "G28" in contentA, f"File {partA_expected} missing expected content 'G28'"

    with open(partB_expected, 'r') as f:
        contentB = f.read()
    assert "E150.9" in contentB, f"File {partB_expected} missing expected content 'E150.9'"
    assert "G28" in contentB, f"File {partB_expected} missing expected content 'G28'"

def test_no_extra_files():
    processed_dir = "/home/user/dataset_processed"
    files = os.listdir(processed_dir)
    # Expected only partA_E7.gcode and partB_E150.gcode
    expected_files = {"partA_E7.gcode", "partB_E150.gcode"}
    actual_files = set(files)

    extra_files = actual_files - expected_files
    assert not extra_files, f"Found unexpected files in {processed_dir}: {extra_files}"