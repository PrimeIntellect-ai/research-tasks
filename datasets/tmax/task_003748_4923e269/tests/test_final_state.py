# test_final_state.py

import os
import re
import pytest

def test_setup_py_modified():
    setup_path = "/home/user/ci_pipeline/math_accel/setup.py"
    assert os.path.isfile(setup_path), f"File {setup_path} does not exist."

    with open(setup_path, "r") as f:
        content = f.read()

    # Check if libraries=['m'] (or equivalent) is present
    # We strip whitespace to be robust against formatting differences
    assert re.search(r"libraries\s*=\s*\[\s*['\"]m['\"]\s*\]", content), \
        "setup.py does not appear to link against the math library (libraries=['m'] is missing)."

def test_extension_built_inplace():
    # Check if the .so file is built in the math_accel/math_accel directory
    ext_dir = "/home/user/ci_pipeline/math_accel/math_accel"
    assert os.path.isdir(ext_dir), f"Directory {ext_dir} does not exist."

    so_files = [f for f in os.listdir(ext_dir) if f.endswith('.so')]
    assert len(so_files) > 0, "The C extension (.so file) was not found in the math_accel/math_accel directory. Was it built in-place?"

def test_version_output():
    out_path = "/home/user/ci_pipeline/version_out.txt"
    assert os.path.isfile(out_path), f"File {out_path} does not exist."

    with open(out_path, "r") as f:
        content = f.read().strip()

    assert content == "1.2.1-beta.11", \
        f"version_out.txt contains '{content}', but expected '1.2.1-beta.11'."

def test_sorted_results():
    sorted_path = "/home/user/ci_pipeline/sorted_results.txt"
    assert os.path.isfile(sorted_path), f"File {sorted_path} does not exist."

    with open(sorted_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"sorted_results.txt should contain exactly 2 lines, found {len(lines)}."

    # Parse the lines
    results = []
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Line '{line}' is not in 'Method,Time' format."
        method = parts[0]
        try:
            time_val = float(parts[1])
        except ValueError:
            pytest.fail(f"Could not parse time value in line: '{line}'")
        results.append((method, time_val))

    # Check sorting
    assert results[0][1] <= results[1][1], "The results are not sorted by execution time in ascending order."

    # Check that CExtension is faster and thus first
    assert results[0][0] == "CExtension", "CExtension should be faster than PurePython and appear first."
    assert results[1][0] == "PurePython", "PurePython should appear second."