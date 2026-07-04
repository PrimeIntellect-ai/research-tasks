# test_final_state.py

import os
import math

def test_fit_model_c_exists():
    """Verify that the C source code file exists."""
    file_path = "/home/user/fit_model.c"
    assert os.path.isfile(file_path), f"Missing required C source file: {file_path}"

def test_coeffs_txt_correct():
    """Verify that coeffs.txt exists and contains the correct coefficients."""
    file_path = "/home/user/coeffs.txt"
    assert os.path.isfile(file_path), f"Missing required output file: {file_path}"

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 coefficients in {file_path}, but found {len(lines)}"

    expected_coeffs = [5.766103, -1.696156, 0.194723, 0.017773]
    tolerance = 0.0005

    for i, (line, expected) in enumerate(zip(lines, expected_coeffs)):
        try:
            val = float(line)
        except ValueError:
            assert False, f"Coefficient at line {i+1} is not a valid float: {line}"

        assert math.isclose(val, expected, abs_tol=tolerance), \
            f"Coefficient c{i} mismatch: expected {expected}, got {val} (tolerance {tolerance})"

def test_fit_png_exists_and_valid():
    """Verify that fit.png exists and is a valid PNG image."""
    file_path = "/home/user/fit.png"
    assert os.path.isfile(file_path), f"Missing required plot file: {file_path}"
    assert os.path.getsize(file_path) > 0, f"The plot file {file_path} is empty."

    with open(file_path, "rb") as f:
        header = f.read(8)

    # PNG magic number: 89 50 4E 47 0D 0A 1A 0A
    png_magic = b'\x89PNG\r\n\x1a\n'
    assert header == png_magic, f"{file_path} is not a valid PNG file based on its header."