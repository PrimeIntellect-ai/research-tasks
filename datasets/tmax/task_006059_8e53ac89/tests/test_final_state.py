# test_final_state.py

import os
import re
import struct

def test_run_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "gcc" in content, f"Script {script_path} does not appear to invoke gcc."
    assert "-lgsl" in content, f"Script {script_path} does not link GSL (-lgsl)."

def test_c_program_exists():
    c_path = "/home/user/etl_filter.c"
    assert os.path.exists(c_path), f"C program {c_path} does not exist."
    assert os.path.isfile(c_path), f"{c_path} is not a file."

def test_pipeline_metrics_correct():
    metrics_path = "/home/user/pipeline_metrics.txt"
    expected_metrics_path = "/tmp/expected_metrics.txt"

    assert os.path.exists(metrics_path), f"Metrics file {metrics_path} does not exist."
    assert os.path.exists(expected_metrics_path), f"Expected metrics file {expected_metrics_path} is missing."

    with open(expected_metrics_path, "r") as f:
        expected_lines = [line.strip() for line in f if line.strip()]

    with open(metrics_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) >= 3, f"Metrics file {metrics_path} does not contain enough lines."

    expected_mean = None
    expected_sd = None
    expected_count = None

    for line in expected_lines:
        if line.startswith("Mean:"):
            expected_mean = float(line.split(":")[1].strip())
        elif line.startswith("SD:"):
            expected_sd = float(line.split(":")[1].strip())
        elif line.startswith("Count:"):
            expected_count = int(line.split(":")[1].strip())

    actual_mean = None
    actual_sd = None
    actual_count = None

    for line in actual_lines:
        if line.startswith("Mean:"):
            actual_mean = float(line.split(":")[1].strip())
        elif line.startswith("SD:"):
            actual_sd = float(line.split(":")[1].strip())
        elif line.startswith("Count:"):
            actual_count = int(line.split(":")[1].strip())

    assert actual_mean is not None, "Mean not found in pipeline_metrics.txt"
    assert actual_sd is not None, "SD not found in pipeline_metrics.txt"
    assert actual_count is not None, "Count not found in pipeline_metrics.txt"

    assert abs(actual_mean - expected_mean) < 1e-5, f"Expected Mean ~ {expected_mean}, got {actual_mean}"
    assert abs(actual_sd - expected_sd) < 1e-5, f"Expected SD ~ {expected_sd}, got {actual_sd}"
    assert actual_count == expected_count, f"Expected Count {expected_count}, got {actual_count}"

def test_output_data_correct():
    output_path = "/home/user/output_data.bin"
    assert os.path.exists(output_path), f"Output data file {output_path} does not exist."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    size = os.path.getsize(output_path)
    expected_size = 9800 * 8
    assert size == expected_size, f"Output file size should be {expected_size} bytes, got {size} bytes."