# test_final_state.py

import os
import subprocess
import math

def test_failing_line_identified():
    failing_line_path = "/home/user/failing_line.txt"
    assert os.path.isfile(failing_line_path), f"File {failing_line_path} is missing."
    with open(failing_line_path, "r") as f:
        content = f.read().strip()
    assert content == "7", f"Expected failing line to be '7', but got '{content}'."

def test_mre_exists_and_reproduces_error():
    mre_path = "/home/user/mre.py"
    assert os.path.isfile(mre_path), f"File {mre_path} is missing."

    # The MRE should reproduce the exact ValueError: math domain error
    result = subprocess.run(
        ["python3", mre_path],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0, "mre.py should fail, but it exited successfully."
    assert "ValueError: math domain error" in result.stderr, "mre.py did not reproduce the 'ValueError: math domain error'."

def test_build_sh_completes_successfully():
    build_sh_path = "/home/user/build.sh"
    assert os.path.isfile(build_sh_path), f"File {build_sh_path} is missing."

    result = subprocess.run(
        [build_sh_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"build.sh failed with output: {result.stderr}"

def test_output_angles_correctness():
    output_path = "/home/user/output_angles.txt"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 8, f"Expected 8 lines in output_angles.txt, but got {len(lines)}."

    try:
        angles = [float(line) for line in lines]
    except ValueError:
        assert False, "output_angles.txt contains non-numeric values."

    # Line 3: 0.0, 0.0, 1.0 | 0.0, 0.0, -1.0 -> 180 degrees (pi radians)
    assert math.isclose(angles[2], math.pi, abs_tol=1e-5), f"Expected line 3 to be ~3.14159, got {angles[2]}"

    # Line 4: 1.0, 1.0, 1.0 | 2.0, 2.0, 2.0 -> 0 degrees
    assert math.isclose(angles[3], 0.0, abs_tol=1e-5), f"Expected line 4 to be 0.0, got {angles[3]}"

    # Line 7: 0.1, 0.2, 0.3 | 0.3, 0.6, 0.9 -> 0 degrees (the edge case)
    assert math.isclose(angles[6], 0.0, abs_tol=1e-5), f"Expected line 7 to be 0.0, got {angles[6]}"