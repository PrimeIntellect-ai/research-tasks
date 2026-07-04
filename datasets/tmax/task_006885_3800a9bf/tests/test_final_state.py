# test_final_state.py
import os
import subprocess

def test_script_exists():
    """Check that the solve_bratu.py script was created."""
    assert os.path.isfile("/home/user/solve_bratu.py"), "The script /home/user/solve_bratu.py does not exist."

def test_run_script_and_check_log():
    """Run the script if needed and verify the output log."""
    log_path = "/home/user/bratu_convergence.log"

    # If the log doesn't exist, try running the script
    if not os.path.isfile(log_path):
        result = subprocess.run(["python3", "/home/user/solve_bratu.py"], capture_output=True, text=True)
        assert result.returncode == 0, f"Script failed to run: {result.stderr}"

    assert os.path.isfile(log_path), f"The log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "N=127, u_mid=0.113954"
    assert content == expected_content, f"Log file content is incorrect. Expected '{expected_content}', but got '{content}'"