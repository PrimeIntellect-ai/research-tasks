# test_final_state.py

import os
import stat
import subprocess
import re

def test_script_exists_and_executable():
    script_path = "/home/user/setup_baseline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    # Run the script to ensure it produces the expected state
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

def test_directories_created():
    dirs = [
        "/home/user/service/www",
        "/home/user/service/logs",
        "/home/user/service/certs"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} was not created."

def test_symlink_created():
    symlink_path = "/home/user/service/current_logs"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    target = os.readlink(symlink_path)
    # The target could be absolute or relative
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), target))
    assert target == "/home/user/service/logs", f"Symlink points to {target} instead of /home/user/service/logs"

def test_certificates_generated():
    cert_path = "/home/user/service/certs/cert.pem"
    key_path = "/home/user/service/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate {cert_path} missing."
    assert os.path.isfile(key_path), f"Private key {key_path} missing."

    with open(cert_path, "r") as f:
        cert_content = f.read()
    assert "BEGIN CERTIFICATE" in cert_content, "cert.pem does not look like a valid PEM certificate."

    with open(key_path, "r") as f:
        key_content = f.read()
    assert "PRIVATE KEY" in key_content, "key.pem does not look like a valid PEM private key."

def test_logrotate_config():
    conf_path = "/home/user/service/logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config {conf_path} missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/service/logs/*.log" in content, "Logrotate config missing target log path."
    assert re.search(r'\bdaily\b', content), "Logrotate config missing 'daily'."
    assert re.search(r'\brotate\s+7\b', content), "Logrotate config missing 'rotate 7'."
    assert re.search(r'\bcompress\b', content), "Logrotate config missing 'compress'."

def test_dummy_log():
    log_path = "/home/user/service/logs/access.log"
    assert os.path.isfile(log_path), f"Dummy log {log_path} missing."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 1000, f"Expected 1000 lines in access.log, found {len(lines)}."
    assert lines[0] == "dummy log entry", "Log entry content does not match expected."

def test_baseline_size():
    size_file = "/home/user/baseline_size.txt"
    assert os.path.isfile(size_file), f"Baseline size file {size_file} missing."

    with open(size_file, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Baseline size file contains non-numeric data: {content}"

    # Verify the size matches the actual du output
    result = subprocess.run(["du", "-sb", "/home/user/service"], capture_output=True, text=True)
    actual_size = result.stdout.split()[0]

    assert content == actual_size, f"Baseline size {content} does not match actual size {actual_size}."