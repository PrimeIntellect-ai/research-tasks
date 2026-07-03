# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.txt")
BUILD_FILE = os.path.join(PROJECT_DIR, "build.sh")

def test_build_script_succeeds():
    """
    Ensure that build.sh can be executed successfully and returns exit code 0.
    """
    assert os.path.isfile(BUILD_FILE), f"File {BUILD_FILE} is missing."
    assert os.access(BUILD_FILE, os.X_OK), f"File {BUILD_FILE} is not executable."

    # Run the build script
    result = subprocess.run([BUILD_FILE], cwd=PROJECT_DIR, capture_output=True, text=True)

    assert result.returncode == 0, (
        f"build.sh failed with exit code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

def test_output_file_correct():
    """
    Ensure that output.txt contains the correct variance.
    """
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} was not created."

    with open(OUTPUT_FILE, "r") as f:
        content = f.read().strip()

    assert content == "0.046667", f"Expected variance '0.046667', but got '{content}' in {OUTPUT_FILE}."

def test_data_and_config_unmodified():
    """
    Ensure the user did not modify config.ini or data.txt.
    """
    config_file = os.path.join(PROJECT_DIR, "config.ini")
    data_file = os.path.join(PROJECT_DIR, "data.txt")

    with open(config_file, "r") as f:
        config_content = f.read()
    assert config_content == "DATA_FILE=/home/user/project/data.txt\n", "config.ini was modified."

    with open(data_file, "r") as f:
        data_content = f.read()
    expected_data = "1000000.1, 1000000.2, 1000000.3,\n1000000.4, 1000000.5\n1000000.6, , 1000000.7\n"
    assert data_content == expected_data, "data.txt was modified."