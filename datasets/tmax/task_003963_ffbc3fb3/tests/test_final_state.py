# test_final_state.py

import os
import subprocess
import time
import socket

def test_check_port_exists_and_executable():
    """Verify that check_port.c and the compiled executable exist."""
    assert os.path.exists("/home/user/check_port.c"), "/home/user/check_port.c does not exist."
    assert os.path.exists("/home/user/check_port"), "/home/user/check_port does not exist."
    assert os.access("/home/user/check_port", os.X_OK), "/home/user/check_port is not executable."

def test_check_port_behavior():
    """Test the behavior of the check_port executable."""
    executable = "/home/user/check_port"

    # Ensure port 8080 is free before starting
    try:
        subprocess.run(["fuser", "-k", "8080/tcp"], capture_output=True)
    except Exception:
        pass

    # Test FAIL state
    result = subprocess.run([executable], capture_output=True, text=True)
    assert result.stdout == "STATUS: FAIL\n", f"Expected 'STATUS: FAIL\\n', got {repr(result.stdout)}"

    # Test OK state
    server = subprocess.Popen(["python3", "-m", "http.server", "8080"])
    try:
        # Wait for the server to start
        for _ in range(10):
            try:
                with socket.create_connection(("127.0.0.1", 8080), timeout=1):
                    break
            except OSError:
                time.sleep(0.5)
        else:
            assert False, "Test server failed to start on port 8080"

        result = subprocess.run([executable], capture_output=True, text=True)
        assert result.stdout == "STATUS: OK\n", f"Expected 'STATUS: OK\\n', got {repr(result.stdout)}"
    finally:
        server.terminate()
        server.wait()

def test_git_repo_and_hook_exist():
    """Verify that the git repository and post-commit hook are configured."""
    repo_dir = "/home/user/monitor_repo"
    hook_path = os.path.join(repo_dir, ".git/hooks/post-commit")

    assert os.path.exists(os.path.join(repo_dir, ".git")), f"Git repository not initialized at {repo_dir}"
    assert os.path.exists(hook_path), f"post-commit hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-commit hook is not executable"

def test_git_hook_behavior():
    """Test the post-commit hook and log rotation."""
    repo_dir = "/home/user/monitor_repo"
    log_file = os.path.join(repo_dir, "net_log.txt")
    bak_file = os.path.join(repo_dir, "net_log.bak")

    # Clean up logs if they exist from previous manual runs
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(bak_file):
        os.remove(bak_file)

    # Ensure port 8080 is closed to get FAIL
    try:
        subprocess.run(["fuser", "-k", "8080/tcp"], capture_output=True)
    except Exception:
        pass

    def make_commit(filename):
        filepath = os.path.join(repo_dir, filename)
        with open(filepath, 'w') as f:
            f.write("test")
        subprocess.run(["git", "add", filename], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", f"Add {filename}"], cwd=repo_dir, check=True, capture_output=True)

    # Commit 1
    make_commit("test1")
    assert os.path.exists(log_file), "net_log.txt was not created after commit."
    with open(log_file, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 1, f"Expected 1 line in net_log.txt, got {len(lines)}"
    assert lines[0] == "STATUS: FAIL\n"

    # Commit 2
    make_commit("test2")
    with open(log_file, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 2, f"Expected 2 lines in net_log.txt, got {len(lines)}"

    # Commit 3
    make_commit("test3")
    assert os.path.exists(log_file), "net_log.txt should exist (even if empty) after 3rd commit."
    with open(log_file, 'r') as f:
        log_content = f.read()
    assert log_content == "", f"net_log.txt should be empty after 3rd commit, got {repr(log_content)}"

    assert os.path.exists(bak_file), "net_log.bak was not created after 3rd commit."
    with open(bak_file, 'r') as f:
        bak_lines = f.readlines()
    assert len(bak_lines) == 3, f"Expected 3 lines in net_log.bak, got {len(bak_lines)}"
    assert all(line == "STATUS: FAIL\n" for line in bak_lines)

    # Commit 4
    make_commit("test4")
    with open(log_file, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 1, f"Expected 1 line in net_log.txt after 4th commit, got {len(lines)}"

    with open(bak_file, 'r') as f:
        bak_lines = f.readlines()
    assert len(bak_lines) == 3, f"Expected 3 lines in net_log.bak after 4th commit, got {len(bak_lines)}"