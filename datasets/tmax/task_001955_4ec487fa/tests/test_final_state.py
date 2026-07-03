# test_final_state.py

import os
import subprocess

def test_git_repo_exists():
    repo_path = "/home/user/uptime_repo.git"
    assert os.path.isdir(repo_path), f"Bare repository directory {repo_path} does not exist."

    # Check if it's a bare git repo
    config_path = os.path.join(repo_path, "config")
    assert os.path.isfile(config_path), f"Git config file not found in {repo_path}."

    with open(config_path, "r") as f:
        content = f.read()
        assert "bare = true" in content.lower(), f"Repository at {repo_path} is not a bare Git repository."

def test_post_receive_hook():
    hook_path = "/home/user/uptime_repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"post-receive hook does not exist at {hook_path}."
    assert os.access(hook_path, os.X_OK), f"post-receive hook at {hook_path} is not executable."

def test_uptime_config():
    config_dir = "/home/user/uptime_config"
    endpoints_file = os.path.join(config_dir, "endpoints.txt")
    assert os.path.isdir(config_dir), f"Configuration directory {config_dir} does not exist."
    assert os.path.isfile(endpoints_file), f"endpoints.txt does not exist in {config_dir}."

    with open(endpoints_file, "r") as f:
        content = f.read()
        assert "http://127.0.0.1:8080/health" in content, "endpoints.txt is missing the 8080 URL."
        assert "http://127.0.0.1:8081/health" in content, "endpoints.txt is missing the 8081 URL."

def test_monitor_bin():
    bin_path = "/home/user/monitor_bin"
    assert os.path.isfile(bin_path), f"Monitor binary does not exist at {bin_path}."
    assert os.access(bin_path, os.X_OK), f"Monitor binary at {bin_path} is not executable."

def test_uptime_results():
    results_file = "/home/user/uptime_results.log"
    assert os.path.isfile(results_file), f"Results log file does not exist at {results_file}."

    with open(results_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_8080 = "http://127.0.0.1:8080/health is UP"
    expected_8081 = "http://127.0.0.1:8081/health is DOWN"

    assert expected_8080 in lines, f"Expected '{expected_8080}' in {results_file}."
    assert expected_8081 in lines, f"Expected '{expected_8081}' in {results_file}."