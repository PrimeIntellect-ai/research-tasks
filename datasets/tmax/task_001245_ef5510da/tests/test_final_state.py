# test_final_state.py
import os
import subprocess

def test_deploy_pipeline():
    # 1. Verify the bare repository
    repo_dir = "/home/user/deploy_repo.git"
    assert os.path.isdir(repo_dir), f"{repo_dir} does not exist"
    result = subprocess.run(
        ["git", "-C", repo_dir, "rev-parse", "--is-bare-repository"], 
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "true", f"{repo_dir} is not a valid bare repository"

    # 2. Verify the deployed executable
    target = "/home/user/deploy_target/updater"
    assert os.path.isfile(target), f"{target} does not exist"
    assert os.access(target, os.X_OK), f"{target} is not executable"

    # 3. Verify the log file for the initial push
    log_file = "/home/user/deploy.log"
    assert os.path.isfile(log_file), f"{log_file} does not exist"

    source_repo = "/home/user/source_repo"
    result = subprocess.run(
        ["git", "-C", source_repo, "rev-parse", "HEAD"], 
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to get HEAD hash from source_repo"
    initial_hash = result.stdout.strip()

    with open(log_file, "r") as f:
        log_contents = f.read()

    assert f"BUILD SUCCESS: {initial_hash}" in log_contents, f"Log missing BUILD SUCCESS for {initial_hash}"
    assert "UPDATER EXECUTED" in log_contents, "Log missing UPDATER EXECUTED"

    # 4. Simulate a push with broken C code to verify error handling
    updater_c = os.path.join(source_repo, "updater.c")
    with open(updater_c, "a") as f:
        f.write("\nsyntax error;\n")

    # Commit the broken code
    subprocess.run(
        ["git", "-C", source_repo, "commit", "-am", "Break build"], 
        capture_output=True
    )

    # Get the new broken commit hash
    result = subprocess.run(
        ["git", "-C", source_repo, "rev-parse", "HEAD"], 
        capture_output=True, text=True
    )
    broken_hash = result.stdout.strip()

    # Push to origin
    push_result = subprocess.run(
        ["git", "-C", source_repo, "push", "origin", "master"], 
        capture_output=True
    )
    assert push_result.returncode != 0, "Push of broken code should have failed (the hook should exit with a non-zero status)"

    # 5. Verify the log file for the failure message
    with open(log_file, "r") as f:
        log_contents = f.read()

    assert f"BUILD FAILED: {broken_hash}" in log_contents, f"Log missing BUILD FAILED for {broken_hash}"