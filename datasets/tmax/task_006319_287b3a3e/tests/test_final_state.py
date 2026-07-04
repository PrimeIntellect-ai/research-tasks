# test_final_state.py
import os
import subprocess

def test_process_c_exists():
    """Test that process.c exists."""
    assert os.path.isfile("/home/user/process.c"), "/home/user/process.c is missing"

def test_run_sh_exists_and_executable():
    """Test that run.sh exists and is executable."""
    assert os.path.isfile("/home/user/run.sh"), "/home/user/run.sh is missing"
    assert os.access("/home/user/run.sh", os.X_OK), "/home/user/run.sh is not executable"

def test_run_sh_execution_and_summary():
    """Test that running run.sh produces the correct summary.csv."""
    # Ensure summary.csv is removed before running to verify run.sh creates it
    if os.path.exists("/home/user/summary.csv"):
        os.remove("/home/user/summary.csv")

    # Run the script
    result = subprocess.run(
        ["./run.sh"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"run.sh failed to execute. stderr: {result.stderr}"

    # Check if summary.csv was created
    assert os.path.isfile("/home/user/summary.csv"), "/home/user/summary.csv was not created by run.sh"

    # Check the content of summary.csv
    expected_content = "ALPHA,20.40\nBETA,10.00\nGAMMA,0.50"

    with open("/home/user/summary.csv", "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The content of /home/user/summary.csv is incorrect.\nExpected:\n{expected_content}\nGot:\n{content}"