# test_final_state.py

import os
import pytest
import struct
import base64
import math

def test_cpp_fixes_applied():
    path = "/home/user/math_util.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # Check that strict weak ordering is fixed (no '<=' in compare function)
    # The student might have changed it to '<'
    assert "a.distance <= b.distance" not in content, "Bug 1 (strict weak ordering) is still present. Use '<' instead of '<='."

    # Check that buffer overflow is fixed
    assert "new Point[num_points - 1]" not in content, "Bug 2 (buffer overflow) is still present. Allocate the correct number of points."

    # Check that memory leak/UB is fixed
    assert "delete points;" not in content, "Bug 3 (wrong delete) is still present. Use 'delete[] points;' or std::vector."

def test_executable_exists():
    path = "/home/user/math_util"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you compile the code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_csv_correct():
    out_path = "/home/user/output.csv"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    b64_path = "/home/user/data.b64"
    assert os.path.isfile(b64_path), f"Data file {b64_path} does not exist."

    with open(b64_path, "r") as f:
        b64_data = f.read().strip()

    bin_data = base64.b64decode(b64_data)

    points = []
    # struct Point { int32_t id; float x; float y; float z; float distance; }; -> 20 bytes
    for i in range(0, len(bin_data), 20):
        chunk = bin_data[i:i+20]
        if len(chunk) < 20:
            break
        pid, x, y, z, _ = struct.unpack("<iffff", chunk)
        dist = math.sqrt(x*x + y*y + z*z)
        points.append((pid, dist))

    points.sort(key=lambda p: p[1])

    expected_lines = []
    for p in points:
        # Match standard C++ float formatting approximately, 
        # but since we just need to match the expected.csv, we can read expected.csv
        pass

    exp_path = "/home/user/expected.csv"
    assert os.path.isfile(exp_path), f"Expected file {exp_path} does not exist."

    with open(exp_path, "r") as f:
        expected_content = f.read().strip().splitlines()

    with open(out_path, "r") as f:
        actual_content = f.read().strip().splitlines()

    assert actual_content == expected_content, "The content of output.csv does not match expected.csv."

def test_diff_result_empty():
    path = "/home/user/diff_result.txt"
    assert os.path.isfile(path), f"Diff result file {path} does not exist."

    size = os.path.getsize(path)
    assert size == 0, f"Diff result file {path} is not empty. This means output.csv does not exactly match expected.csv."