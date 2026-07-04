# test_final_state.py

import os
import subprocess
import pytest

def test_organizer_files_exist():
    """Check that the C++ source and compiled executable exist."""
    assert os.path.isfile('/home/user/organizer.cpp'), "Source file /home/user/organizer.cpp is missing."
    assert os.path.isfile('/home/user/organizer'), "Compiled executable /home/user/organizer is missing."
    assert os.access('/home/user/organizer', os.X_OK), "/home/user/organizer is not executable."

def test_performance_and_state_verification():
    """Run the verification script to test performance and system state."""
    # Run the verification script which generates 50,000 files, runs the organizer, and checks the state
    result = subprocess.run(['/app/verify_performance.sh'], capture_output=True, text=True)
    output = result.stdout + "\n" + result.stderr

    # Check for state validation failures from the bash script
    assert "State validation failed" not in output, f"State validation failed during verification. Output:\n{output}"

    # Extract execution time
    execution_time = None
    for line in output.splitlines():
        if line.startswith("execution_time:"):
            try:
                execution_time = float(line.split(":")[1].strip())
            except ValueError:
                pass
            break

    assert execution_time is not None, f"Could not parse execution_time from script output. Output:\n{output}"

    # Verify the metric threshold
    assert execution_time <= 3.0, f"Execution time {execution_time} seconds exceeded the 3.0 seconds threshold."

    # Ensure the script exited successfully (PASS)
    assert result.returncode == 0, f"verify_performance.sh failed with exit code {result.returncode}. Output:\n{output}"
    assert "PASS" in output, f"Expected PASS in output, but got:\n{output}"