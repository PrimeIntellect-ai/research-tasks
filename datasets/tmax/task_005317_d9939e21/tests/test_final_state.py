# test_final_state.py

import os
import subprocess

def test_files_exist():
    """Check that all required files exist."""
    assert os.path.isfile("/home/user/divergence.py"), "/home/user/divergence.py is missing."
    assert os.path.isfile("/home/user/run_parallel.sh"), "/home/user/run_parallel.sh is missing."
    assert os.path.isfile("/home/user/test_divergence.py"), "/home/user/test_divergence.py is missing."

def test_run_parallel_and_log():
    """Run run_parallel.sh and verify kl_results.log contents."""
    # Ensure the script is executable or run it via bash
    subprocess.run(["bash", "/home/user/run_parallel.sh"], check=True)

    assert os.path.isfile("/home/user/kl_results.log"), "/home/user/kl_results.log was not created."

    with open("/home/user/kl_results.log", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    lines.sort()
    expected_lines = [
        "-0.5,2.0,0.3494",
        "0.5,1.5,0.1832",
        "1.0,1.0,0.5000",
        "2.0,0.8,3.1831"
    ]

    assert lines == expected_lines, f"kl_results.log contents do not match expected. Got: {lines}"

def test_pytest_execution():
    """Run pytest on test_divergence.py and check for success."""
    result = subprocess.run(["pytest", "/home/user/test_divergence.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"pytest /home/user/test_divergence.py failed:\n{result.stdout}\n{result.stderr}"

def test_divergence_script_output():
    """Run divergence.py with specific arguments and check output."""
    result = subprocess.run(
        ["python3", "/home/user/divergence.py", "--mu", "0.0", "--sigma", "1.0"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"divergence.py failed to run:\n{result.stderr}"

    output = result.stdout.strip()
    # The output could be 0.0,1.0,0.0000
    assert output == "0.0,1.0,0.0000", f"Expected '0.0,1.0,0.0000', got '{output}'"