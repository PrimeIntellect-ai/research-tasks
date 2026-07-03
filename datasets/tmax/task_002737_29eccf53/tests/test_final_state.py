# test_final_state.py
import os
import math

def test_fftw_installed():
    """Verify that FFTW was installed locally in /home/user/fftw."""
    include_file = "/home/user/fftw/include/fftw3.h"
    lib_file_a = "/home/user/fftw/lib/libfftw3.a"
    lib_file_so = "/home/user/fftw/lib/libfftw3.so"

    assert os.path.exists(include_file), f"FFTW include file not found at {include_file}"
    assert os.path.exists(lib_file_a) or os.path.exists(lib_file_so), \
        "FFTW library file (libfftw3.a or libfftw3.so) not found in /home/user/fftw/lib/"

def test_c_program_exists():
    """Verify that the C program source file exists."""
    c_file = "/home/user/wave_profiler.c"
    assert os.path.exists(c_file), f"C program not found at {c_file}"

def test_result_file():
    """Verify that the result.txt file exists and contains the correct KL divergence value."""
    result_file = "/home/user/result.txt"
    assert os.path.exists(result_file), f"Result file not found at {result_file}"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content != "", "Result file is empty."

    try:
        val = float(content)
    except ValueError:
        assert False, f"Result file content '{content}' is not a valid float."

    expected_val = 3.023402
    assert math.isclose(val, expected_val, abs_tol=1e-5), \
        f"Expected result to be close to {expected_val}, but got {val}"