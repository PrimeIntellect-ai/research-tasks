# test_final_state.py
import os
import subprocess

def test_rollout_go_exists():
    assert os.path.isfile("/home/user/rollout.go"), "/home/user/rollout.go does not exist."

def test_rollout_behavior():
    # Compile the Go program
    compile_result = subprocess.run(
        ["go", "build", "-o", "rollout", "rollout.go"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"Failed to compile rollout.go:\n{compile_result.stderr}"

    # Ensure clean state
    state_file = "/home/user/rollout.state"
    log_file = "/home/user/deployed_env.log"
    if os.path.exists(state_file):
        os.remove(state_file)
    if os.path.exists(log_file):
        os.remove(log_file)

    # Run the compiled binary
    run_result = subprocess.run(
        ["./rollout"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert run_result.returncode == 0, f"rollout failed with exit code {run_result.returncode}:\n{run_result.stderr}"

    # Check state file
    assert os.path.isfile(state_file), f"{state_file} was not created."
    with open(state_file, "r") as f:
        state_content = f.read()
    assert state_content == "SUCCESS_beta", f"State file content is '{state_content}', expected 'SUCCESS_beta'."

    # Check log file
    assert os.path.isfile(log_file), f"{log_file} was not created by the legacy script."
    with open(log_file, "r") as f:
        log_content = f.read().strip()
    assert log_content == "beta", f"Log file content is '{log_content}', expected 'beta'."

    # Run again to test idempotency
    run_result_2 = subprocess.run(
        ["./rollout"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert run_result_2.returncode == 0, f"Second run failed with exit code {run_result_2.returncode}."
    assert "Already deployed" in run_result_2.stdout, "Expected 'Already deployed' in output on second run."

    # Test early exit by removing log file
    os.remove(log_file)
    run_result_3 = subprocess.run(
        ["./rollout"],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert run_result_3.returncode == 0, f"Third run failed with exit code {run_result_3.returncode}."
    assert not os.path.exists(log_file), "The legacy script was executed again despite the state file indicating success."