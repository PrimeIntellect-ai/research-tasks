# test_final_state.py
import os
import hashlib

def test_pipeline_script_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."

def test_symlink_and_binary():
    symlink_path = "/home/user/deploy/current"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target_path = os.path.realpath(symlink_path)
    assert os.path.isfile(target_path), f"Symlink target {target_path} does not exist or is not a file."
    assert os.access(target_path, os.X_OK), f"Symlink target {target_path} is not executable."

    assert target_path.startswith("/home/user/deploy/releases/"), \
        f"Symlink target {target_path} is not inside /home/user/deploy/releases/"

    # Calculate hash and size of the binary
    with open(target_path, "rb") as f:
        data = f.read()

    binary_size = len(data)
    binary_hash = hashlib.sha256(data).hexdigest()

    expected_filename = f"mailer_daemon_{binary_hash}"
    assert os.path.basename(target_path) == expected_filename, \
        f"Binary filename {os.path.basename(target_path)} does not match expected {expected_filename}."

def test_alert_email_file():
    symlink_path = "/home/user/deploy/current"
    assert os.path.exists(symlink_path), "Symlink does not exist, cannot verify email contents."
    target_path = os.path.realpath(symlink_path)

    with open(target_path, "rb") as f:
        data = f.read()
    binary_size = len(data)
    binary_hash = hashlib.sha256(data).hexdigest()

    email_path = "/home/user/alerts/deploy_email.txt"
    assert os.path.isfile(email_path), f"Alert file {email_path} does not exist."

    with open(email_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "To: devops@company.local",
        "Subject: Deployment successful",
        f"Binary-Size: {binary_size}",
        f"Checksum: {binary_hash}"
    ]

    for expected_line in expected_lines:
        assert expected_line in lines, f"Expected line '{expected_line}' not found in {email_path}."