# test_final_state.py

import os
import subprocess

def test_ticket_resolution_content():
    """Verify that ticket_resolution.txt contains the correct IP and byte count."""
    path = "/home/user/ticket_resolution.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you save the output?"

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "10.0.0.99,5600"
    assert content == expected, f"Expected '{expected}' in {path}, but got '{content}'."

def test_analyze_script_fixed():
    """Verify that the analyze.py script has been fixed and produces the correct output."""
    script_path = "/home/user/analyze.py"
    capture_path = "/home/user/network_capture.txt"

    assert os.path.isfile(script_path), f"File {script_path} is missing."
    assert os.path.isfile(capture_path), f"File {capture_path} is missing."

    result = subprocess.run(
        ["python3", script_path, capture_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    output = result.stdout.strip()
    expected = "10.0.0.99,5600"

    assert output == expected, f"Expected script to output '{expected}', but got '{output}'. The off-by-one error may not be fully fixed."