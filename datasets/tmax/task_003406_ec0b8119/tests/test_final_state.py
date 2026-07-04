# test_final_state.py

import os
import subprocess
import tempfile

def test_git_repo_exists():
    """Ensure the Git repository exists."""
    assert os.path.isdir("/home/user/manifest-repo/.git"), "Git repository was not initialized at /home/user/manifest-repo."

def test_git_hook_executable():
    """Ensure the post-commit hook exists and is executable."""
    hook_path = "/home/user/manifest-repo/.git/hooks/post-commit"
    assert os.path.isfile(hook_path), f"Hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Hook at {hook_path} is not executable."

def test_commit_exists():
    """Ensure the commit was successful with the correct message."""
    repo_dir = "/home/user/manifest-repo"
    try:
        output = subprocess.check_output(
            ["git", "log", "--oneline"],
            cwd=repo_dir,
            text=True,
            stderr=subprocess.STDOUT
        )
        assert "Add initial network manifest" in output, "The required commit message was not found in the git log."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run git log in {repo_dir}: {e.output}")

def test_initial_hook_execution():
    """Verify the initial commit triggered the hook and populated the spool file."""
    spool_file = "/home/user/mail_spool.txt"
    assert os.path.isfile(spool_file), f"{spool_file} does not exist. Hook may not have run."
    with open(spool_file, "r") as f:
        content = f.read()
    assert "ALERT: Invalid route 10.0.0.1 rejected" in content, f"Expected alert not found in {spool_file}."

def test_operator_binary_behavior():
    """Test the C++ binary independently for correct behaviors."""
    binary_path = "/home/user/operator"
    assert os.path.isfile(binary_path), f"Operator binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Operator at {binary_path} is not executable."

    with tempfile.TemporaryDirectory() as temp_dir:
        # Test 1: Valid route
        conf_path = os.path.join(temp_dir, "network-manifest.conf")
        with open(conf_path, "w") as f:
            f.write("default_route=192.168.1.254\n")

        # Run operator
        result = subprocess.run([binary_path], cwd=temp_dir, capture_output=True)
        assert result.returncode == 0, "Operator did not exit with status 0 for valid route."

        log_file = "/home/user/active_network.log"
        assert os.path.isfile(log_file), f"{log_file} was not created."
        with open(log_file, "r") as f:
            log_content = f.read()
        assert log_content == "ROUTE_ACCEPTED\n", f"Expected 'ROUTE_ACCEPTED\\n' in {log_file}, got {repr(log_content)}"

        # Test 2: Invalid route (silent rejection)
        with open(conf_path, "w") as f:
            f.write("default_route=8.8.8.8\n")

        result = subprocess.run([binary_path], cwd=temp_dir, capture_output=True)
        assert result.returncode == 0, "Operator did not exit with status 0 for invalid route."

        spool_file = "/home/user/mail_spool.txt"
        assert os.path.isfile(spool_file), f"{spool_file} was not created."
        with open(spool_file, "r") as f:
            spool_content = f.read()
        assert "ALERT: Invalid route 8.8.8.8 rejected\n" in spool_content, f"Expected rejection alert not found in {spool_file}."

        # Test 3: Missing file
        os.remove(conf_path)
        result = subprocess.run([binary_path], cwd=temp_dir, capture_output=True)
        assert result.returncode == 0, "Operator did not exit with status 0 when file is missing."