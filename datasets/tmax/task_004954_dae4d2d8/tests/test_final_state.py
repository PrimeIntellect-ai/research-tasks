# test_final_state.py

import os
import re
import math

def test_c_source_exists():
    """Test that the C source code file exists."""
    src_path = "/home/user/process_pdb.c"
    assert os.path.isfile(src_path), f"C source file {src_path} is missing."

def test_executable_exists():
    """Test that the compiled executable exists and is executable."""
    exe_path = "/home/user/process_pdb"
    assert os.path.isfile(exe_path), f"Executable {exe_path} is missing. Did you compile the code?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_output_file_exists_and_correct():
    """Test that the output.txt file exists and contains the correctly formatted and calculated results."""
    out_path = "/home/user/output.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing. Did you run the program?"

    with open(out_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, "output.txt should contain at least 2 lines (one for Left domain, one for Right domain)."

    # We check the last two lines in case the user ran the program multiple times and appended.
    left_line = lines[-2]
    right_line = lines[-1]

    # Regex to parse the expected format
    pattern = r"Domain (Left|Right):\s*N_atoms=(\d+),\s*det=([0-9\.\-eE]+),\s*status=(OK|SINGULAR)"

    # Check Left Domain
    match_left = re.match(pattern, left_line)
    assert match_left, f"Left domain line format is incorrect. Got: '{left_line}'"
    assert match_left.group(1) == "Left", f"Expected 'Left' domain, got '{match_left.group(1)}'"
    assert match_left.group(2) == "4", f"Expected N_atoms=4 for Left domain, got {match_left.group(2)}"

    det_left = float(match_left.group(3))
    assert math.isclose(det_left, 0.0, abs_tol=1e-4), f"Left domain determinant incorrect. Expected ~0.0, got {det_left}"
    assert match_left.group(4) == "SINGULAR", f"Expected status=SINGULAR for Left domain, got {match_left.group(4)}"

    # Check Right Domain
    match_right = re.match(pattern, right_line)
    assert match_right, f"Right domain line format is incorrect. Got: '{right_line}'"
    assert match_right.group(1) == "Right", f"Expected 'Right' domain, got '{match_right.group(1)}'"
    assert match_right.group(2) == "4", f"Expected N_atoms=4 for Right domain, got {match_right.group(2)}"

    det_right = float(match_right.group(3))
    assert math.isclose(det_right, 8.109375, rel_tol=1e-3, abs_tol=1e-3), f"Right domain determinant incorrect. Expected ~8.109375, got {det_right}"
    assert match_right.group(4) == "OK", f"Expected status=OK for Right domain, got {match_right.group(4)}"