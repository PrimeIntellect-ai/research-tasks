# test_final_state.py
import os
import subprocess
import json

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. The pipeline may not have run successfully."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "PIPELINE_PASSED" in content, f"Expected 'PIPELINE_PASSED' in {log_path}, got: {content}"

def test_pre_commit_hook():
    hook_path = "/home/user/app_repo/.git/hooks/pre-commit"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_check_quota_sh():
    script_path = "/home/user/app_repo/check_quota.sh"
    db_path = "/home/user/app_repo/users.db"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Save original db content to restore later
    with open(db_path, "rb") as f:
        original_db = f.read()

    try:
        # Test with small db (<= 1024 bytes)
        with open(db_path, "wb") as f:
            f.write(b"0" * 500)

        res_ok = subprocess.run([script_path], cwd="/home/user/app_repo", capture_output=True, text=True)
        assert res_ok.returncode == 0, f"check_quota.sh should exit with 0 for files <= 1024 bytes, got {res_ok.returncode}"
        assert "QUOTA_OK" in res_ok.stdout, f"Expected 'QUOTA_OK' in stdout for small file, got {res_ok.stdout}"

        # Test with large db (> 1024 bytes)
        with open(db_path, "wb") as f:
            f.write(b"0" * 1025)

        res_exceeded = subprocess.run([script_path], cwd="/home/user/app_repo", capture_output=True, text=True)
        assert res_exceeded.returncode == 1, f"check_quota.sh should exit with 1 for files > 1024 bytes, got {res_exceeded.returncode}"
        assert "QUOTA_EXCEEDED" in res_exceeded.stdout, f"Expected 'QUOTA_EXCEEDED' in stdout for large file, got {res_exceeded.stdout}"
    finally:
        # Restore original db
        with open(db_path, "wb") as f:
            f.write(original_db)

def test_config_json():
    config_path = "/home/user/app_repo/config.json"
    assert os.path.isfile(config_path), f"{config_path} does not exist."
    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{config_path} does not contain valid JSON."

    assert config.get("auth_port") == 8123, f"auth_port in config.json is not set to 8123 (got {config.get('auth_port')})."

def test_git_commit():
    repo_path = "/home/user/app_repo"
    res = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo_path, capture_output=True, text=True)
    assert res.returncode == 0, "Failed to run git log. Is it a valid git repository?"
    assert "Fix pipeline" in res.stdout, f"The latest commit message does not contain 'Fix pipeline'. Got: {res.stdout}"