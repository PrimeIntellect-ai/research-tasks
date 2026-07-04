# test_final_state.py
import os
import tarfile
import subprocess

def test_git_repo_exists():
    """Verify that the Git repository was created."""
    git_dir = "/home/user/finops_pipeline/.git"
    assert os.path.isdir(git_dir), f"Git repository not found at {git_dir}"

def test_backup_dir_exists():
    """Verify that the backup directory was created."""
    backup_dir = "/home/user/backups"
    assert os.path.isdir(backup_dir), f"Backup directory not found at {backup_dir}"

def test_pre_commit_hook_exists_and_executable():
    """Verify that the pre-commit hook exists and is executable."""
    hook_path = "/home/user/finops_pipeline/.git/hooks/pre-commit"
    assert os.path.isfile(hook_path), f"pre-commit hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-commit hook at {hook_path} is not executable"

def test_backup_file_created_and_valid():
    """Verify that the backup tarball was created and contains the CSV file."""
    backup_file = "/home/user/backups/raw_backup_latest.tar.gz"
    assert os.path.isfile(backup_file), f"Backup file not found at {backup_file}"

    try:
        with tarfile.open(backup_file, "r:gz") as tar:
            names = tar.getnames()
            # The file could be archived with or without a leading path, but it should be named input_billing.csv
            assert any(name.endswith("input_billing.csv") for name in names), \
                f"input_billing.csv not found in the backup tarball. Contents: {names}"
    except tarfile.ReadError:
        assert False, f"Backup file {backup_file} is not a valid gzip-compressed tarball"

def test_network_daily_costs_log_content():
    """Verify that the network daily costs log has the correctly aggregated and formatted data."""
    log_path = "/home/user/finops_pipeline/network_daily_costs.log"
    assert os.path.isfile(log_path), f"Log file not found at {log_path}"

    expected_lines = [
        "2023-10-14: $5.50",
        "2023-10-15: $12.25",
        "2023-10-16: $8.00",
        "2023-10-17: $20.00"
    ]

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, \
        f"Content of {log_path} does not match expected output.\nExpected: {expected_lines}\nActual: {actual_lines}"

def test_git_commit_exists():
    """Verify that the initial commit was made with the correct message."""
    repo_dir = "/home/user/finops_pipeline"
    try:
        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True
        )
        assert "Add initial billing data" in result.stdout, \
            f"Commit message 'Add initial billing data' not found in git log. Log output:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to run 'git log' in {repo_dir}. Error: {e.stderr}"