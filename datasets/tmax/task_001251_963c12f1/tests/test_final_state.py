# test_final_state.py

import os

def test_analyze_script_exists():
    """Verify that the analyze.py script was created."""
    script_path = "/home/user/analyze.py"
    assert os.path.isfile(script_path), f"The analysis script was not found at {script_path}."

def test_malware_output_exists():
    """Verify that the malware output file was created."""
    output_path = "/home/user/malware_output.txt"
    assert os.path.isfile(output_path), f"The malware output file was not found at {output_path}."

def test_malware_output_content():
    """Verify that the malware output contains the expected sandboxed execution result."""
    output_path = "/home/user/malware_output.txt"
    assert os.path.isfile(output_path), "Cannot check content because output file does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_string = "EVIDENCE_FLAG: Network isolated successfully. Executing safe local payload."
    assert expected_string in content, (
        f"The output file does not contain the expected evidence flag.\n"
        f"Expected to find: '{expected_string}'\n"
        f"Actual content: '{content}'"
    )