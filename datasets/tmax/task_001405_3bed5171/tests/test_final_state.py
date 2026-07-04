# test_final_state.py

import os
import pytest

def test_aggregate_executable_exists():
    executable_path = "/home/user/aggregate"
    assert os.path.isfile(executable_path), f"Executable {executable_path} not found. Did you compile the C code?"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_aggregate_c_is_fixed():
    file_path = "/home/user/aggregate.c"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    assert "int sums[5]" not in content, "The bug 'int sums[5]' is still present in aggregate.c."
    assert "double sums" in content or "float sums" in content, "Could not find a floating-point 'sums' array declaration in aggregate.c."

def test_centroid_output_correct():
    input_file = "/home/user/embeddings.csv"
    output_file = "/home/user/centroid.csv"

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did you run the compiled executable?"

    # Calculate expected centroid
    sums = [0.0] * 5
    count = 0
    with open(input_file, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) == 5:
                for i in range(5):
                    sums[i] += float(parts[i])
                count += 1

    assert count > 0, f"No valid data found in {input_file}."

    expected = [s / count for s in sums]
    expected_str = ",".join([f"{x:.4f}" for x in expected])

    with open(output_file, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, f"Centroid output incorrect. Expected: '{expected_str}', Actual: '{actual_str}'"