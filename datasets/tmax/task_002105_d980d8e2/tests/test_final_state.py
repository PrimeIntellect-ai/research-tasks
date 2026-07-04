# test_final_state.py

import os
import json
import subprocess

def get_latest_commit_hash():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd="/home/user/infra.git",
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def test_infra_git_is_bare_repo():
    assert os.path.isdir("/home/user/infra.git"), "/home/user/infra.git directory is missing."
    result = subprocess.run(
        ["git", "rev-parse", "--is-bare-repository"],
        cwd="/home/user/infra.git",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0 and result.stdout.strip() == "true", "/home/user/infra.git is not a valid bare Git repository."

def test_custom_fstab_contents():
    fstab_path = "/home/user/custom.fstab"
    assert os.path.isfile(fstab_path), f"{fstab_path} is missing."

    with open(fstab_path, "r") as f:
        content = f.read()

    expected_line_1 = "/home/user/data /mnt/app_data ext4 defaults 0 0"
    expected_line_2 = "/home/user/logs /mnt/app_logs tmpfs defaults 0 0"

    assert expected_line_1 in content, f"Expected mount line '{expected_line_1}' not found in {fstab_path}."
    assert expected_line_2 in content, f"Expected mount line '{expected_line_2}' not found in {fstab_path}."

def test_container_status_json():
    status_path = "/home/user/container_status.json"
    assert os.path.isfile(status_path), f"{status_path} is missing."

    with open(status_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{status_path} does not contain valid JSON."

    hash_val = get_latest_commit_hash()
    assert hash_val is not None, "Could not retrieve the latest commit hash from /home/user/infra.git."

    assert data.get("running") is True, f"'running' should be true in {status_path}."
    assert data.get("last_deployed_commit") == hash_val, f"'last_deployed_commit' should be '{hash_val}' in {status_path}."

def test_mail_out_conf():
    conf_path = "/home/user/mail_out.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    hash_val = get_latest_commit_hash()
    assert hash_val is not None, "Could not retrieve the latest commit hash from /home/user/infra.git."

    expected_to = "To: sysadmin@local.domain"
    expected_subject = f"Subject: Deployment for commit {hash_val}"
    expected_status = "Status: Success"

    assert expected_to in content, f"Expected line '{expected_to}' not found in {conf_path}."
    assert expected_subject in content, f"Expected line '{expected_subject}' not found in {conf_path}."
    assert expected_status in content, f"Expected line '{expected_status}' not found in {conf_path}."