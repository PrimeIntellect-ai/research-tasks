# test_final_state.py

import os
import math

def test_mathops_c_patched():
    path = "/home/user/math_utils/mathops.c"
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, 'r') as f:
        content = f.read()
    assert "x = 0.5 * (x + n / x);" in content or "x = (x + n / x) / 2" in content or "0.5" in content, \
        "mathops.c does not contain the corrected logic from the patch"

def test_cmake_links_math_library():
    path = "/home/user/math_utils/CMakeLists.txt"
    assert os.path.isfile(path), f"{path} is missing"
    with open(path, 'r') as f:
        content = f.read()
    assert "target_link_libraries" in content and "m" in content, \
        "CMakeLists.txt does not link the math library (target_link_libraries missing or 'm' not linked)"

def test_shared_library_built():
    path = "/home/user/math_utils/build/libmathops.so"
    assert os.path.isfile(path), f"Shared library {path} was not built"

def test_result_file_correct():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"{path} is missing. The result was not saved."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content, f"{path} is empty"

    try:
        val = float(content)
    except ValueError:
        assert False, f"Content of {path} is not a valid float: {content}"

    # Compute expected value based on the truth logic
    x = 612.0
    for _ in range(10):
        x = 0.5 * (x + 612.0 / x)

    assert abs(val - x) < 1e-5, f"Value in {path} ({val}) does not match the expected computed square root (~{x})"