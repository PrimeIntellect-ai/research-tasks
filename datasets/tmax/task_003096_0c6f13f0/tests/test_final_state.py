# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_result_file_correct():
    result_file = "/home/user/ticket_8841/result.txt"
    assert os.path.isfile(result_file), f"Result file missing: {result_file}"

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content == "770", f"Expected result to be '770', but got '{content}'"

def test_script_behavior_fixed():
    script_path = "/home/user/ticket_8841/sum_values.sh"
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    # Create a temporary directory with spaces in filenames to test the script's robustness
    with tempfile.TemporaryDirectory() as temp_dir:
        spaces_dir = os.path.join(temp_dir, "test dir with spaces")
        os.makedirs(spaces_dir)

        file1 = os.path.join(spaces_dir, "file A.txt")
        file2 = os.path.join(spaces_dir, "fileB.txt")

        with open(file1, "w") as f:
            f.write("5\n")
        with open(file2, "w") as f:
            f.write("10\n")

        # Total sum = 15. We set MATH_SCALE=3, expected output = 45.
        env = os.environ.copy()
        env["MATH_SCALE"] = "3"

        try:
            result = subprocess.run(
                [script_path, temp_dir],
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout.strip()
            assert output == "45", f"Script did not produce the correct output for test data. Expected '45', got '{output}'"
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Script execution failed: {e.stderr}")