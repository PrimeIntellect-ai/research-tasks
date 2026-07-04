# test_final_state.py
import os
import json
import subprocess

def test_metric_logger_c_exists():
    path = '/home/user/metric_logger.c'
    assert os.path.isfile(path), f"{path} does not exist."

def test_metric_logger_executable_exists():
    path = '/home/user/metric_logger'
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_push_metric_exp_executable_exists():
    path = '/home/user/push_metric.exp'
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_post_commit_hook_executable_exists():
    path = '/home/user/dash_config/.git/hooks/post-commit'
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_dashboard_metrics_log_contents():
    path = '/home/user/dashboard_metrics.log'
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, 'r') as f:
        lines = f.readlines()

    found = False
    for line in lines:
        try:
            data = json.loads(line.strip())
            if data.get("metric") == "dashboard_updates" and data.get("value") == 1:
                found = True
                break
        except json.JSONDecodeError:
            continue

    assert found, f"Expected JSON log entry not found in {path}."

def test_dash_json_exists_and_content():
    path = '/home/user/dash_config/dash.json'
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
        assert data.get("refresh") == 5, "dash.json does not contain the expected content."
    except json.JSONDecodeError:
        assert False, "dash.json does not contain valid JSON."

def test_git_commit_made():
    repo_dir = '/home/user/dash_config'
    assert os.path.isdir(os.path.join(repo_dir, '.git')), f"Git repository not initialized in {repo_dir}."

    result = subprocess.run(
        ['git', 'log', '--oneline'],
        cwd=repo_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, "Failed to run git log. Are there any commits?"
    assert len(result.stdout.strip().split('\n')) >= 1, "No commits found in the repository."