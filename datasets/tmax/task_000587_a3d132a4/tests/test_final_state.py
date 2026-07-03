# test_final_state.py

import os
import subprocess

def test_weights_file():
    """Verify that weights.txt exists and has the correct exact content."""
    file_path = "/home/user/weights.txt"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "CPU=2.50 MEM=1.20 IO=4.00"
    assert content == expected_content, f"Content of {file_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_visualize_script_exists_and_executable():
    """Verify that visualize.sh exists and is executable."""
    file_path = "/home/user/visualize.sh"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_visualize_script_output():
    """Verify the output of visualize.sh matches the expected format."""
    file_path = "/home/user/visualize.sh"

    # Run the script
    result = subprocess.run([file_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {file_path} failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.strip()

    expected_lines = [
        "Row 1: Pred=69.00 Actual: ******",
        "Row 2: Pred=145.00 Actual: **************",
        "Row 3: Pred=138.00 Actual: *************",
        "Row 4: Pred=231.00 Actual: ***********************",
        "Row 5: Pred=210.00 Actual: *********************"
    ]

    output_lines = [line.strip() for line in output.split("\n") if line.strip()]

    for i, expected_line in enumerate(expected_lines):
        assert i < len(output_lines), f"Missing output line. Expected: '{expected_line}'"
        assert output_lines[i] == expected_line, f"Output line {i+1} is incorrect. Expected '{expected_line}', got '{output_lines[i]}'."