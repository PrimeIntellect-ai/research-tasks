# test_final_state.py

import os
import stat
import pytest
import csv

def test_c_code_fixed():
    c_file = "/home/user/src/clean_join.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."

    with open(c_file, "r") as f:
        content = f.read()

    # The bug was using %f to read into double variables. It should be %lf.
    assert "%lf" in content, "The C code does not appear to be fixed. Hint: use '%lf' to read into 'double' variables with fscanf."
    assert "%d,%lf,%lf" in content.replace(" ", ""), "The calibration fscanf format string is not correctly fixed."
    assert "%d,%[^,],%lf" in content.replace(" ", ""), "The sensor fscanf format string is not correctly fixed."

def test_pipeline_script_exists_and_executable():
    script_file = "/home/user/pipeline.sh"
    assert os.path.isfile(script_file), f"Pipeline script {script_file} is missing."

    st = os.stat(script_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"Pipeline script {script_file} is not executable."

def test_final_output_correct():
    sensors_file = "/home/user/data/sensors.csv"
    calibration_file = "/home/user/data/calibration.csv"
    output_file = "/home/user/output/final_data.csv"

    assert os.path.isfile(sensors_file), f"Input file {sensors_file} missing."
    assert os.path.isfile(calibration_file), f"Input file {calibration_file} missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did the pipeline run successfully?"

    # Recompute expected output
    calibrations = {}
    with open(calibration_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split(",")
            calibrations[parts[0]] = (float(parts[1]), float(parts[2]))

    expected_rows = []
    with open(sensors_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split(",")
            s_id = parts[0]
            timestamp = parts[1]
            val = float(parts[2])

            offset, multiplier = calibrations.get(s_id, (0.0, 1.0))
            cleaned_value = (val + offset) * multiplier
            expected_rows.append((int(s_id), timestamp, f"{cleaned_value:.2f}"))

    # Sort numerically by id (first column)
    expected_rows.sort(key=lambda x: x[0])
    expected_output = [f"{r[0]},{r[1]},{r[2]}" for r in expected_rows]

    # Read actual output
    with open(output_file, "r") as f:
        actual_output = [line.strip() for line in f if line.strip()]

    assert actual_output == expected_output, (
        f"Output data in {output_file} does not match expected sorted output.\n"
        f"Expected:\n{chr(10).join(expected_output)}\n\n"
        f"Actual:\n{chr(10).join(actual_output)}"
    )