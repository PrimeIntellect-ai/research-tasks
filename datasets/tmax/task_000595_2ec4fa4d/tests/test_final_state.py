# test_final_state.py
import os
import stat
import subprocess
import pytest
import pandas as pd
import numpy as np

def test_loads_csv_metric():
    """Test that loads.csv is generated and MSE is within threshold."""
    csv_path = '/home/user/workspace/loads.csv'
    assert os.path.exists(csv_path), f"File not found: {csv_path}"

    truth_loads = np.array([
        45.0, 52.1, 60.5, 42.0, 39.5, 70.2, 85.0, 91.5, 40.0, 38.5, 
        45.6, 50.0, 55.5, 60.1, 62.3, 75.0, 80.0, 82.5, 88.0, 95.5, 
        30.0, 35.5, 40.0, 42.5, 45.0, 50.0, 52.5, 60.0, 65.5, 70.0
    ])

    try:
        df = pd.read_csv(csv_path)
        assert 'Load' in df.columns, "CSV must contain a 'Load' column"
        agent_loads = df['Load'].values
        assert len(agent_loads) == 30, f"Expected 30 rows in CSV, found {len(agent_loads)}"

        mse = np.mean((truth_loads - agent_loads) ** 2)
    except Exception as e:
        pytest.fail(f"Failed to read or parse {csv_path}: {e}")

    assert mse <= 1.5, f"MSE {mse} exceeds threshold of 1.5"

def test_git_repo_and_commits():
    """Test that git repo exists and files are committed."""
    workspace = '/home/user/workspace'
    assert os.path.exists(os.path.join(workspace, '.git')), "Git repository not initialized"

    # Check if files are committed
    status = subprocess.run(
        ['git', 'ls-files'], 
        cwd=workspace, 
        capture_output=True, 
        text=True
    )
    assert status.returncode == 0, "Git ls-files command failed"
    committed_files = status.stdout.splitlines()
    assert 'decode.py' in committed_files, "decode.py is not committed to the repository"
    assert 'loads.csv' in committed_files, "loads.csv is not committed to the repository"

def test_pre_commit_hook():
    """Test that pre-commit hook exists and is executable."""
    hook_path = '/home/user/workspace/.git/hooks/pre-commit'
    assert os.path.exists(hook_path), f"pre-commit hook not found at {hook_path}"

    st = os.stat(hook_path)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"pre-commit hook at {hook_path} is not executable"

def test_cron_job():
    """Test that the cron job is configured correctly."""
    status = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    # It might be empty or not exist, which returns non-zero, but we just check stdout if zero
    # If no crontab for user, it might fail, which means task not done.
    assert status.returncode == 0, "Failed to read crontab or no crontab configured"

    crontab_content = status.stdout
    assert '0 2 * * *' in crontab_content, "Cron schedule '0 2 * * *' not found in crontab"
    assert '/home/user/workspace/decode.py' in crontab_content, "Script path not found in crontab"