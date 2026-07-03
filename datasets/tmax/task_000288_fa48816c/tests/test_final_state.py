# test_final_state.py

import os
import zipfile
import re
import tempfile
import pytest

RAW_DATA_DIR = "/home/user/raw_data"
ZIP_PATH = "/home/user/final_project.zip"
WAL_LOG_PATH = "/home/user/process_wal.log"
SCALE_FACTOR = 1.75
TOLERANCE = 0.005

def get_valid_gcode_files():
    valid_files = []
    if not os.path.isdir(RAW_DATA_DIR):
        return valid_files

    for root, _, files in os.walk(RAW_DATA_DIR):
        for f in files:
            if f.endswith(".gcode"):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        lines = [file.readline() for _ in range(5)]
                        if any("; TYPE: PART" in line for line in lines):
                            valid_files.append(path)
                except Exception:
                    pass
    return valid_files

def parse_coordinates(line):
    # Find all X, Y, Z coordinates
    coords = {}
    for match in re.finditer(r'([XYZ])([-+]?[0-9]*\.?[0-9]+)', line):
        coords[match.group(1)] = float(match.group(2))
    return coords

def test_final_project_zip_exists():
    assert os.path.isfile(ZIP_PATH), f"Final project zip not found at {ZIP_PATH}"

def test_wal_log_correctness():
    assert os.path.isfile(WAL_LOG_PATH), f"WAL log not found at {WAL_LOG_PATH}"

    valid_files = get_valid_gcode_files()
    expected_basenames = set(os.path.basename(f) for f in valid_files)

    with open(WAL_LOG_PATH, "r", encoding="utf-8") as f:
        log_lines = [line.strip() for line in f if line.strip()]

    log_basenames = []
    for line in log_lines:
        assert line.startswith("PROCESSED: "), f"Invalid log line format: {line}"
        log_basenames.append(line.replace("PROCESSED: ", "").strip())

    assert len(log_basenames) == len(expected_basenames), f"Expected {len(expected_basenames)} log entries, found {len(log_basenames)}."
    assert set(log_basenames) == expected_basenames, "Log entries do not match the expected valid GCode files."

def test_gcode_scaling_metric():
    valid_files = get_valid_gcode_files()
    assert len(valid_files) > 0, "No valid GCode files found in raw_data to test against."

    max_error = 0.0

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        for orig_path in valid_files:
            basename = os.path.basename(orig_path)
            student_path = os.path.join(tmpdir, basename)

            assert os.path.isfile(student_path), f"Expected scaled file {basename} not found in zip."

            with open(orig_path, "r", encoding="utf-8") as f_orig, \
                 open(student_path, "r", encoding="utf-8") as f_stud:

                orig_lines = f_orig.readlines()
                stud_lines = f_stud.readlines()

                assert len(orig_lines) == len(stud_lines), f"Line count mismatch in {basename}"

                for i, (orig_line, stud_line) in enumerate(zip(orig_lines, stud_lines)):
                    orig_coords = parse_coordinates(orig_line)
                    stud_coords = parse_coordinates(stud_line)

                    for axis in orig_coords:
                        assert axis in stud_coords, f"Missing {axis} coordinate in {basename} line {i+1}"
                        expected_val = orig_coords[axis] * SCALE_FACTOR
                        actual_val = stud_coords[axis]
                        error = abs(expected_val - actual_val)
                        if error > max_error:
                            max_error = error

    assert max_error <= TOLERANCE, f"Max absolute error {max_error} exceeds tolerance {TOLERANCE}"