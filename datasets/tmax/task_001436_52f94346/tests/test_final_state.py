# test_final_state.py

import os
import subprocess

def test_test_script_success():
    """Run test.sh and ensure it returns 0 and outputs BUILD SUCCESS."""
    test_sh_path = "/home/user/project/test.sh"
    assert os.path.isfile(test_sh_path), f"{test_sh_path} is missing"

    result = subprocess.run(
        [test_sh_path],
        cwd="/home/user/project",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"test.sh failed with return code {result.returncode}. Output:\n{result.stdout}\n{result.stderr}"
    assert "BUILD SUCCESS" in result.stdout, "test.sh did not output 'BUILD SUCCESS'"

def test_output_matches_expected():
    """Ensure output.txt matches expected.txt after running the pipeline."""
    output_path = "/home/user/project/output.txt"
    expected_path = "/home/user/project/expected.txt"

    assert os.path.isfile(output_path), f"{output_path} is missing"
    assert os.path.isfile(expected_path), f"{expected_path} is missing"

    with open(output_path, "r") as f:
        output_content = f.read().strip()

    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    assert output_content == expected_content, f"Contents of {output_path} do not match {expected_path}"

def test_compute_c_fixed():
    """Ensure the bug in compute.c has been modified."""
    compute_c_path = "/home/user/project/compute.c"
    assert os.path.isfile(compute_c_path), f"{compute_c_path} is missing"

    with open(compute_c_path, "r") as f:
        content = f.read()

    # The original bug had a plus sign: b*b + 4*a*c
    # We check that the exact original buggy line is no longer there, or the logic changed.
    # Since whitespace can vary, we strip spaces for a basic check.
    content_no_spaces = content.replace(" ", "")
    assert "b*b+4*a*c" not in content_no_spaces, "The mathematical bug (b*b + 4*a*c) is still present in compute.c"