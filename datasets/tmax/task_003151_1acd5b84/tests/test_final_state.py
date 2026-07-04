# test_final_state.py

import os
import stat
import glob
import subprocess
import pytest

def get_expected_crashing_file() -> str:
    """
    Derives the expected crashing file by looking for the 'DEAD' magic bytes
    that trigger the panic in the data_extractor binary.
    """
    data_dir = "/home/user/suspicious_data"
    if not os.path.exists(data_dir):
        return "/home/user/suspicious_data/payload_37.dat"

    for filepath in glob.glob(os.path.join(data_dir, "*.dat")):
        if filepath.endswith("_extracted.dat"):
            continue
        try:
            with open(filepath, "r", errors="ignore") as f:
                if f.read(4) == "DEAD":
                    return filepath
        except Exception:
            continue
    return "/home/user/suspicious_data/payload_37.dat"

def test_crashing_file_identified_correctly():
    """
    Validates that the student correctly identified the payload causing the crash
    and wrote its absolute path to /home/user/crashing_file.txt.
    """
    result_file = "/home/user/crashing_file.txt"
    assert os.path.isfile(result_file), f"The result file {result_file} does not exist."

    with open(result_file, "r") as f:
        student_answer = f.read().strip()

    expected_file = get_expected_crashing_file()
    assert student_answer == expected_file, (
        f"Incorrect crashing file identified.\n"
        f"Expected: {expected_file}\n"
        f"Found: {student_answer}"
    )

def test_analyze_fixed_script_exists_and_executable():
    """
    Validates that /home/user/analyze_fixed.sh exists and has execute permissions.
    """
    script_path = "/home/user/analyze_fixed.sh"
    assert os.path.isfile(script_path), f"The fixed script {script_path} does not exist."

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"The fixed script {script_path} is not executable."

def test_analyze_fixed_script_execution_and_termination():
    """
    Executes the fixed script to ensure it terminates (no infinite loop)
    and successfully processes the valid data files.
    """
    script_path = "/home/user/analyze_fixed.sh"
    data_dir = "/home/user/suspicious_data"

    # Ensure the script is executable before running
    if not os.access(script_path, os.X_OK):
        pytest.fail(f"Cannot execute {script_path} because it lacks execute permissions.")

    # Run the script with a timeout to catch infinite loops
    try:
        # We run it in the /home/user directory as the original script assumes relative paths or cd
        proc = subprocess.run(
            [script_path],
            cwd="/home/user",
            timeout=10,
            capture_output=True,
            text=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {script_path} timed out after 10 seconds. The infinite loop bug is likely still present.")

    # Verify that the script actually processed files by checking for the presence of _extracted.dat files
    extracted_files = glob.glob(os.path.join(data_dir, "*_extracted.dat"))

    assert len(extracted_files) > 0, (
        f"The script {script_path} completed, but no *_extracted.dat files were found in {data_dir}. "
        "It appears the script did not successfully process the valid payloads."
    )