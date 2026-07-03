# test_final_state.py

import os
import subprocess
import pytest

def test_flag_file_content():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"The file {flag_path} does not exist."

    with open(flag_path, "r") as f:
        content = f.read()

    assert content == "FLAG{d3bug_m3}", f"The content of {flag_path} is incorrect. Found: {repr(content)}"

def test_decoder_script_fixed():
    script_path = "/home/user/decoder.py"
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

    # Run the script with the correct key (42) to verify it has been fixed
    try:
        result = subprocess.run(
            ["python3", script_path, "42"],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The decoder.py script timed out. It likely still has an infinite recursion or loop.")

    assert result.returncode == 0, f"The decoder.py script failed to execute. Error: {result.stderr}"

    output = result.stdout.strip()
    assert output == "FLAG{d3bug_m3}", f"The decoder.py script did not output the correct flag. Found: {repr(output)}"