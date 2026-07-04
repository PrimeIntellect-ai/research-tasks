# test_final_state.py

import os
import pytest

PIPELINE_DIR = "/home/user/etl_pipeline"
RAW_DIR = os.path.join(PIPELINE_DIR, "raw")
MASKED_DIR = os.path.join(PIPELINE_DIR, "masked")
AGGREGATE_FILE = os.path.join(PIPELINE_DIR, "aggregate.csv")
MASKER_C = os.path.join(PIPELINE_DIR, "masker.c")
MASKER_EXEC = os.path.join(PIPELINE_DIR, "masker")
MAKEFILE = os.path.join(PIPELINE_DIR, "Makefile")

RAW_FILES = {
    "raw_data1.csv": [
        "2023-10-01T10:00:00,SENSOR_A,USER_123,22.5",
        "2023-10-01T10:01:00,SENSOR_B,USER_456,23.1",
        "2023-10-01T10:02:00,SENSOR_A,USER_123,22.7"
    ],
    "raw_data2.csv": [
        "2023-10-01T10:03:00,SENSOR_C,USER_789,19.8",
        "2023-10-01T10:04:00,SENSOR_A,USER_001,21.0"
    ],
    "raw_data3.csv": [
        "2023-10-01T10:05:00,SENSOR_B,USER_456,23.5",
        "2023-10-01T10:06:00,SENSOR_C,USER_999,19.2"
    ]
}

def djb2(s):
    h = 5381
    for c in s:
        h = ((h << 5) + h + ord(c)) & 0xFFFFFFFF
    return f"{h:08x}"

def get_expected_masked_content(raw_lines):
    masked_lines = []
    for line in raw_lines:
        parts = line.strip().split(',')
        if len(parts) >= 3:
            parts[2] = djb2(parts[2])
        masked_lines.append(",".join(parts))
    return masked_lines

def test_source_files_exist():
    assert os.path.exists(MASKER_C), f"Source file {MASKER_C} is missing."
    assert os.path.exists(MAKEFILE), f"Makefile {MAKEFILE} is missing."

def test_executable_exists():
    assert os.path.exists(MASKER_EXEC), f"Executable {MASKER_EXEC} is missing. Was it compiled?"
    assert os.access(MASKER_EXEC, os.X_OK), f"File {MASKER_EXEC} is not executable."

def test_masked_directory_exists():
    assert os.path.exists(MASKED_DIR), f"Directory {MASKED_DIR} is missing."
    assert os.path.isdir(MASKED_DIR), f"Path {MASKED_DIR} is not a directory."

@pytest.mark.parametrize("filename, raw_lines", RAW_FILES.items())
def test_masked_files(filename, raw_lines):
    masked_filepath = os.path.join(MASKED_DIR, filename)
    assert os.path.exists(masked_filepath), f"Masked file {masked_filepath} is missing."

    with open(masked_filepath, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = get_expected_masked_content(raw_lines)
    assert actual_lines == expected_lines, f"Content mismatch in {masked_filepath}."

def test_aggregate_file():
    assert os.path.exists(AGGREGATE_FILE), f"Aggregate file {AGGREGATE_FILE} is missing."

    with open(AGGREGATE_FILE, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = []
    for filename in ["raw_data1.csv", "raw_data2.csv", "raw_data3.csv"]:
        expected_lines.extend(get_expected_masked_content(RAW_FILES[filename]))

    assert actual_lines == expected_lines, f"Content mismatch in {AGGREGATE_FILE}."