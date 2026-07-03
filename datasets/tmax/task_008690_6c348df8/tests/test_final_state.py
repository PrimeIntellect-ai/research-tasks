# test_final_state.py
import os
import stat
import subprocess
import tempfile
import pytest

def test_binary_exists_and_executable():
    binary_path = "/home/user/src/audit_processor"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_binary_logic():
    binary_path = "/home/user/src/audit_processor"

    with tempfile.NamedTemporaryFile() as secure_file:
        os.chmod(secure_file.name, 0o600)
        result = subprocess.run([binary_path, secure_file.name], capture_output=True, text=True)
        assert result.returncode == 0, f"Expected exit code 0 for 0600 file, got {result.returncode}"
        assert result.stdout.strip() == "SECURE", f"Expected 'SECURE' output, got '{result.stdout.strip()}'"

    with tempfile.NamedTemporaryFile() as insecure_file:
        os.chmod(insecure_file.name, 0o644)
        result = subprocess.run([binary_path, insecure_file.name], capture_output=True, text=True)
        assert result.returncode == 1, f"Expected exit code 1 for non-0600 file, got {result.returncode}"
        assert result.stdout.strip() == "INSECURE", f"Expected 'INSECURE' output, got '{result.stdout.strip()}'"

    result_missing = subprocess.run([binary_path, "/tmp/does_not_exist_xyz123"], capture_output=True, text=True)
    assert result_missing.returncode == 1, "Expected exit code 1 for missing file."

def test_deploy_script_exists():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script {script_path} does not exist."

def test_deploy_log():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    expected = "Staging: SUCCESS\nProd: SUCCESS"
    assert content == expected, f"Log content mismatch. Expected:\n{expected}\nGot:\n{content}"

def test_deploy_directories():
    dirs = [
        "/home/user/deploy/staging",
        "/home/user/deploy/prod_a",
        "/home/user/deploy/prod_b"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_deployed_files_permissions_and_content():
    envs = ["staging", "prod_a", "prod_b"]
    for env in envs:
        bin_path = f"/home/user/deploy/{env}/audit_processor"
        cfg_path = f"/home/user/deploy/{env}/config.txt"

        assert os.path.isfile(bin_path), f"Binary missing in {env}: {bin_path}"
        st_bin = os.stat(bin_path)
        assert stat.S_IMODE(st_bin.st_mode) == 0o500, f"Binary in {env} must have 0500 permissions."

        assert os.path.isfile(cfg_path), f"Config missing in {env}: {cfg_path}"
        st_cfg = os.stat(cfg_path)
        assert stat.S_IMODE(st_cfg.st_mode) == 0o600, f"Config in {env} must have 0600 permissions."

        with open(cfg_path, "r") as f:
            content = f.read().strip()
        assert content == "v1", f"Config in {env} must contain 'v1'."