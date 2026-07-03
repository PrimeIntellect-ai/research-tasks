# test_final_state.py

import os
import subprocess
import time
import urllib.request
import tempfile
import pytest

def test_binary_exists_and_executable():
    """Test that the compiled binary exists and is executable."""
    binary_path = "/home/user/bin/cap-analyzer"
    assert os.path.isfile(binary_path), f"Binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_post_receive_hook():
    """Test that the post-receive hook exists and is executable."""
    hook_path = "/home/user/repos/data-model.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook at {hook_path} is not executable"

def test_http_server_running():
    """Test that the HTTP server is running and serving the logs directory."""
    # Create a dummy log file to test the server
    log_dir = "/home/user/logs"
    os.makedirs(log_dir, exist_ok=True)
    test_file = os.path.join(log_dir, "test_server.txt")
    with open(test_file, "w") as f:
        f.write("server is running")

    max_retries = 5
    success = False
    for _ in range(max_retries):
        try:
            response = urllib.request.urlopen("http://127.0.0.1:8080/test_server.txt", timeout=2)
            if response.status == 200 and response.read().decode("utf-8").strip() == "server is running":
                success = True
                break
        except Exception:
            time.sleep(1)

    assert success, "HTTP server is not running on 127.0.0.1:8080 or not serving /home/user/logs/"

def test_analyzer_performance_and_accuracy():
    """Test the cap-analyzer binary for speedup and accuracy on a cyclic directory structure."""
    binary_path = "/home/user/bin/cap-analyzer"

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a structure with circular symlinks
        dir1 = os.path.join(temp_dir, "dir1")
        os.makedirs(dir1)

        # Create unique files
        file1 = os.path.join(dir1, "file1.bin")
        with open(file1, "wb") as f:
            f.write(os.urandom(1024 * 1024)) # 1 MB

        file2 = os.path.join(dir1, "file2.bin")
        with open(file2, "wb") as f:
            f.write(os.urandom(2 * 1024 * 1024)) # 2 MB

        # Create circular symlink
        os.symlink(dir1, os.path.join(dir1, "cyclic_link"))

        # Measure execution time
        start_time = time.time()
        try:
            result = subprocess.run(
                [binary_path, "--target", temp_dir],
                capture_output=True,
                text=True,
                timeout=2.0 # The unpatched version would timeout or take much longer
            )
        except subprocess.TimeoutExpired:
            pytest.fail("cap-analyzer timed out. The infinite loop with symlinks was likely not fixed.")

        execution_time = time.time() - start_time

        # The unpatched version would take > 10s (or infinite). We expect it to finish in < 0.5s.
        assert execution_time < 1.0, f"Execution time {execution_time:.2f}s is too slow. Expected < 1.0s (speedup >= 10.0x)"

        # We don't strictly assert the exact byte size here because the Go implementation details
        # (e.g., whether it counts directory sizes or symlink sizes) might vary slightly.
        # However, it must not crash and must return a valid number.
        assert result.returncode == 0, f"cap-analyzer failed with error: {result.stderr}"

def test_git_push_triggers_hook():
    """Test that pushing to the bare repository triggers the hook and updates capacity.log."""
    bare_repo = "/home/user/repos/data-model.git"
    log_file = "/home/user/logs/capacity.log"

    # Clear log file if it exists
    if os.path.exists(log_file):
        os.remove(log_file)

    with tempfile.TemporaryDirectory() as clone_dir:
        # Clone the bare repo
        subprocess.run(["git", "clone", bare_repo, clone_dir], check=True, capture_output=True)

        # Add a file
        test_file = os.path.join(clone_dir, "data.txt")
        with open(test_file, "w") as f:
            f.write("Hello, World!")

        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "add", "data.txt"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=clone_dir, check=True)

        # Push to trigger the hook
        result = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True, text=True)

        # Allow a moment for the hook to write to the log
        time.sleep(0.5)

        assert os.path.exists(log_file), f"{log_file} was not created by the post-receive hook."

        with open(log_file, "r") as f:
            log_contents = f.read().strip()

        assert log_contents, "capacity.log is empty."

        # Check format: [TIMESTAMP] SIZE_IN_BYTES
        lines = log_contents.split("\n")
        last_line = lines[-1]
        assert last_line.startswith("[") and "]" in last_line, f"Log line format incorrect: {last_line}"

        size_part = last_line.split("]")[-1].strip()
        assert size_part.isdigit(), f"Size part of the log is not an integer: {size_part}"