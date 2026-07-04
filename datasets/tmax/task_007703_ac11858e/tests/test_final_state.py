# test_final_state.py

import os
import subprocess
import re

def test_cpp_source_exists():
    """Check if the C++ source file was created."""
    assert os.path.isfile("/home/user/process.cpp"), "/home/user/process.cpp is missing."

def test_executable_exists_and_runs():
    """Check if the executable exists and can be run successfully."""
    exe_path = "/home/user/process"
    assert os.path.isfile(exe_path), f"{exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

    # Run the executable to generate the output
    result = subprocess.run([exe_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {exe_path} failed with return code {result.returncode}. Stderr: {result.stderr}"

def test_output_tsv_correct():
    """Check if the output TSV file is correctly formatted and deduplicated."""
    output_path = "/home/user/output/deduped.tsv"
    assert os.path.isfile(output_path), f"{output_path} was not created."

    expected_lines = [
        "3600\ten\tHello world",
        "3600\tes\tHola mundo",
        "3600\tfr\tBonjour",
        "7200\ten\tHello world",
        "7200\tzh\t你好",
        "7200\tzh\t你好吗"
    ]

    with open(output_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip("\n") for line in f if line.strip("\n")]

    assert actual_lines == expected_lines, "The contents of deduped.tsv do not match the expected deduplicated output."

def test_cron_file_correct():
    """Check if the cron configuration file has the correct schedule."""
    cron_path = "/home/user/mycron"
    assert os.path.isfile(cron_path), f"{cron_path} is missing."

    with open(cron_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Match the cron expression: 0 2 * * * /home/user/process
    # Allow for multiple spaces/tabs between fields
    pattern = r"^0\s+2\s+\*\s+\*\s+\*\s+/home/user/process$"
    match = re.search(pattern, content, re.MULTILINE)

    assert match is not None, f"{cron_path} does not contain the correct cron expression. Found: {content}"