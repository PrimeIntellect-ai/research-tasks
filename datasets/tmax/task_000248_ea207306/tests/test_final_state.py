# test_final_state.py
import os
import pytest

def test_output_file_exists():
    output_path = "/home/user/data_pipeline/output.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did you run the script and redirect the output?"

def test_output_file_content():
    output_path = "/home/user/data_pipeline/output.txt"
    assert os.path.isfile(output_path), "Output file missing."

    expected_lines = [
        "101 cycle detected",
        "102 cycle detected",
        "103 cycle detected",
        "201 terminates normally",
        "202 terminates normally",
        "301 cycle detected",
        "401 terminates normally",
        "402 terminates normally",
        "403 terminates normally"
    ]

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, (
        f"The content of {output_path} does not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(lines)}"
    )

def test_process_script_is_bash():
    script_path = "/home/user/data_pipeline/process.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that it's not a python or perl script
    assert "import " not in content or "python" not in content.splitlines()[0].lower(), "The script appears to be written in Python. It must be written in Bash."
    assert "perl" not in content.splitlines()[0].lower(), "The script appears to be written in Perl. It must be written in Bash."