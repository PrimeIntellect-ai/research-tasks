# test_final_state.py

import os
import subprocess

PROJECT_DIR = "/home/user/project"
CRASH_INFO = os.path.join(PROJECT_DIR, "crash_info.txt")
BUILD_STATUS = os.path.join(PROJECT_DIR, "build_status.txt")
BUILD_SH = os.path.join(PROJECT_DIR, "build.sh")
OUTPUT_LOG = os.path.join(PROJECT_DIR, "output.log")

def test_crash_info_correct():
    assert os.path.exists(CRASH_INFO), f"{CRASH_INFO} is missing. You must create it."
    with open(CRASH_INFO, "r") as f:
        content = f.read().strip()
    assert content == "4", f"Expected {CRASH_INFO} to contain '4', but found '{content}'."

def test_build_status_correct():
    assert os.path.exists(BUILD_STATUS), f"{BUILD_STATUS} is missing. Did you run build.sh?"
    with open(BUILD_STATUS, "r") as f:
        content = f.read().strip()
    assert "Build Success" in content, f"Expected {BUILD_STATUS} to contain 'Build Success'."

def test_processor_fixes_and_build_succeeds():
    assert os.path.exists(BUILD_SH), f"{BUILD_SH} is missing."
    assert os.access(BUILD_SH, os.X_OK), f"{BUILD_SH} is not executable."

    # Run the build script to ensure it compiles and runs successfully
    result = subprocess.run(
        [BUILD_SH],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"build.sh failed with exit code {result.returncode}."

    # Verify that the processor successfully read all 6 records (0 through 5)
    assert os.path.exists(OUTPUT_LOG), f"{OUTPUT_LOG} was not generated."
    with open(OUTPUT_LOG, "r") as f:
        log_content = f.read()

    assert "Record 0" in log_content, "Record 0 was not processed."
    assert "Record 4" in log_content, "Record 4 (the oversized record) was not processed. It must be handled without crashing."
    assert "Record 5" in log_content, "Record 5 was not processed. Ensure the file pointer is correctly advanced after an oversized record."