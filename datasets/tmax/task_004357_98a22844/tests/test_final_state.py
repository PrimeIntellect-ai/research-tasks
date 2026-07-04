# test_final_state.py

import os
import subprocess
import random
import string
import shutil
import tempfile

def test_repo_git_exists():
    assert os.path.isdir("/home/user/repo.git"), "/home/user/repo.git directory does not exist"
    # Check if it's a bare repo
    config_path = "/home/user/repo.git/config"
    assert os.path.exists(config_path), "Git config not found in /home/user/repo.git"
    with open(config_path, "r") as f:
        assert "bare = true" in f.read().lower(), "/home/user/repo.git is not a bare repository"

def test_post_receive_hook_exists_and_executable():
    hook_path = "/home/user/repo.git/hooks/post-receive"
    assert os.path.exists(hook_path), "post-receive hook does not exist"
    assert os.access(hook_path, os.X_OK), "post-receive hook is not executable"

def test_workspace_exists():
    assert os.path.isdir("/home/user/workspace/.git"), "/home/user/workspace is not a git repository"
    assert os.path.exists("/home/user/workspace/filter.go"), "filter.go not found in workspace"

def test_filter_binary_exists():
    assert os.path.exists("/home/user/filter"), "/home/user/filter binary does not exist"
    assert os.access("/home/user/filter", os.X_OK), "/home/user/filter is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_filter"
    agent_path = "/home/user/filter"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"

    random.seed(42)
    charset = string.ascii_letters + string.digits + string.punctuation + " "

    for _ in range(1000):
        length = random.randint(5, 150)
        fuzz_str = "".join(random.choice(charset) for _ in range(length))

        # Run oracle
        oracle_res = subprocess.run(
            [oracle_path, fuzz_str],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_res.stdout.strip()

        # Run agent
        agent_res = subprocess.run(
            [agent_path, fuzz_str],
            capture_output=True,
            text=True
        )
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: {repr(fuzz_str)}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )

def test_git_hook_functionality():
    # Test that pushing to the repo actually triggers the build
    workspace_dir = "/home/user/workspace"
    test_go_code = """package main
import "fmt"
func main() {
    fmt.Print("HOOK_TEST_SUCCESS")
}
"""
    # Create a temporary clone to test push
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["git", "clone", "/home/user/repo.git", tmpdir], check=True, capture_output=True)

        with open(os.path.join(tmpdir, "filter.go"), "w") as f:
            f.write(test_go_code)

        subprocess.run(["git", "add", "filter.go"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-m", "Test hook"], cwd=tmpdir, check=True, capture_output=True)

        # Push to trigger hook
        subprocess.run(["git", "push", "origin", "main"], cwd=tmpdir, check=True, capture_output=True)

    # Check if the binary was updated and outputs the new string
    agent_path = "/home/user/filter"
    assert os.path.exists(agent_path), "Agent binary missing after push"

    res = subprocess.run([agent_path, "dummy"], capture_output=True, text=True)
    assert "HOOK_TEST_SUCCESS" in res.stdout, "The post-receive hook did not correctly compile and deploy the pushed code"