# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/malware_analysis"
DECODER_BIN = os.path.join(BASE_DIR, "decoder")
CRASH_BIN = os.path.join(BASE_DIR, "crash.bin")
REPORT_FILE = os.path.join(BASE_DIR, "report.txt")

def test_makefile_compilation():
    """Verify that the Makefile has been fixed and successfully compiles the decoder."""
    # Ensure we are starting clean
    subprocess.run(["make", "clean"], cwd=BASE_DIR, capture_output=True)

    # Run make
    result = subprocess.run(["make"], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed to execute successfully. stderr: {result.stderr}"

    # Check if the binary was produced
    assert os.path.isfile(DECODER_BIN), f"The 'decoder' executable was not found at {DECODER_BIN} after running make."

    # Check if the missing symbol was linked (log_action from utils.cpp)
    # nm might not be installed, but we can verify execution in the next test.
    # We will check if it's executable.
    assert os.access(DECODER_BIN, os.X_OK), f"The 'decoder' file at {DECODER_BIN} is not executable."

def test_decoder_execution_patched():
    """Verify that the vulnerability is patched and the program exits with code 255 (-1)."""
    # Ensure the binary and test file exist before running
    assert os.path.isfile(DECODER_BIN), "Cannot test execution: decoder binary is missing."
    assert os.path.isfile(CRASH_BIN), "Cannot test execution: crash.bin is missing."

    # Run the decoder with the malformed payload
    result = subprocess.run([DECODER_BIN, CRASH_BIN], cwd=BASE_DIR, capture_output=True)

    # A segmentation fault typically returns 139. We expect 255 (which is -1 cast to unsigned byte).
    assert result.returncode != 139, "The decoder still crashes with a segmentation fault (exit code 139)."
    assert result.returncode == 255, f"Expected decoder to exit with code 255 (-1), but got {result.returncode}."

def test_report_content():
    """Verify the contents of report.txt contain the correct line number and vulnerability type."""
    assert os.path.isfile(REPORT_FILE), f"The report file was not found at {REPORT_FILE}."

    with open(REPORT_FILE, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"The report file at {REPORT_FILE} must contain at least two lines."

    # Check Line 1: The exact line number of the crash
    line1 = lines[0].strip()
    assert line1 == "20", f"Line 1 of report.txt is incorrect. Expected '20', got '{line1}'."

    # Check Line 2: The underlying C++ data type issue
    line2 = lines[1].strip().lower()
    valid_keywords = ["sign", "integer", "negative"]
    has_keyword = any(keyword in line2 for keyword in valid_keywords)
    assert has_keyword, (
        f"Line 2 of report.txt does not identify the correct vulnerability type. "
        f"Expected to find a keyword like 'sign', 'integer', or 'negative'. Got: '{lines[1].strip()}'"
    )