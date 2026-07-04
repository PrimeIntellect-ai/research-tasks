# test_final_state.py
import os
import subprocess
import socket
import time
import tempfile
import pytest

def test_cost_wrapper():
    wrapper = "/home/user/cost_wrapper.exp"
    assert os.path.isfile(wrapper), f"Wrapper script missing at {wrapper}"
    assert os.access(wrapper, os.X_OK), "Wrapper script is not executable"

    # Test eu-west 5 -> 100
    res = subprocess.run([wrapper, "eu-west", "5"], capture_output=True, text=True)
    assert res.returncode == 0, "Wrapper script failed to execute"
    assert res.stdout.strip() == "100", f"Expected wrapper to output '100', got {res.stdout.strip()}"

def test_cost_daemon_tcp():
    # Send request to daemon
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", 9000))
        s.sendall(b"us-east 12\n")
        data = s.recv(1024)
        assert data.decode('utf-8').strip() == "120", f"Expected daemon to return '120', got {data}"
    finally:
        s.close()

def test_supervisor_restarts_daemon():
    # Find process listening on 9000 and kill it
    try:
        pid_str = subprocess.check_output(["lsof", "-t", "-i:9000"]).decode('utf-8').strip()
        if pid_str:
            for pid in pid_str.split():
                os.kill(int(pid), 9)
    except Exception:
        pass # lsof might fail if not found, or process already dead

    # Wait for supervisor to restart it
    time.sleep(2)

    # Test connection again
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(("127.0.0.1", 9000))
        s.sendall(b"eu-west 10\n")
        data = s.recv(1024)
        assert data.decode('utf-8').strip() == "200", "Daemon did not recover after being killed"
    finally:
        s.close()

def test_git_hook_enforcement():
    repo_dir = "/home/user/infra.git"
    assert os.path.isdir(repo_dir), f"Git repo missing at {repo_dir}"

    hook_path = os.path.join(repo_dir, "hooks", "pre-receive")
    assert os.path.isfile(hook_path), f"pre-receive hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), "pre-receive hook is not executable"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo
        subprocess.run(["git", "clone", repo_dir, tmpdir], check=True, capture_output=True)

        # Setup git config
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)

        conf_path = os.path.join(tmpdir, "deployment.conf")

        # Test 1: Reject push (us-east 100 = 1000 > 500)
        with open(conf_path, "w") as f:
            f.write("us-east 100\n")
        subprocess.run(["git", "add", "deployment.conf"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Exceed budget"], cwd=tmpdir, check=True)

        push_res = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert push_res.returncode != 0, "Git push should have been rejected for exceeding budget"
        assert "FinOps: Budget exceeded" in push_res.stderr, "Expected rejection message not found in stderr"

        # Reset commit
        subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=tmpdir, check=True)

        # Test 2: Accept push (eu-west 10 = 200 <= 500)
        with open(conf_path, "w") as f:
            f.write("eu-west 10\n")
        subprocess.run(["git", "add", "deployment.conf"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Within budget"], cwd=tmpdir, check=True)

        push_res2 = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert push_res2.returncode == 0, f"Git push should have succeeded, but failed: {push_res2.stderr}"