# test_final_state.py
import os
import re

def test_orbit_fixed_c_exists():
    """Check if the fixed C file exists."""
    assert os.path.exists("/home/user/orbit_fixed.c"), "The file /home/user/orbit_fixed.c does not exist."
    assert os.path.isfile("/home/user/orbit_fixed.c"), "/home/user/orbit_fixed.c is not a regular file."

def test_orbit_fixed_executable_exists():
    """Check if the compiled executable exists."""
    assert os.path.exists("/home/user/orbit_fixed"), "The compiled executable /home/user/orbit_fixed does not exist."
    assert os.access("/home/user/orbit_fixed", os.X_OK), "The file /home/user/orbit_fixed is not executable."

def test_orbit_result_txt():
    """Check if the result file exists and contains the correct output."""
    assert os.path.exists("/home/user/orbit_result.txt"), "The file /home/user/orbit_result.txt does not exist."
    with open("/home/user/orbit_result.txt", "r") as f:
        content = f.read().strip()
    assert content == "24.73863", f"Expected output '24.73863', but got '{content}'."

def test_orbit_fixed_c_content():
    """Check if the fixed C file meets the requirements."""
    with open("/home/user/orbit_fixed.c", "r") as f:
        content = f.read()

    # Check for double precision
    assert "double" in content, "The fixed program must use 'double' precision variables."

    # Check for tolerance check
    assert "fabs" in content, "The fixed program must use 'fabs' for the convergence check."
    assert "1e-6" in content.lower() or "0.000001" in content, "The fixed program must use a 1e-6 tolerance check."

    # Check for assertion and loop counter
    assert "assert" in content, "The fixed program must use 'assert'."
    assert "1000" in content, "The fixed program must check for iterations < 1000."

    # Check for memory leak fix
    malloc_count = len(re.findall(r'\bmalloc\b', content))
    free_count = len(re.findall(r'\bfree\b', content))

    if malloc_count > 0:
        assert free_count >= malloc_count, "There is a malloc without a corresponding free, indicating a potential memory leak."