# test_final_state.py

import os
import subprocess
from datetime import datetime
import pytest

def test_capacity_report():
    report_path = "/home/user/capacity_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} is missing."
    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "10.0.0.5: 350000",
        "172.16.0.2: 45000",
        "192.168.1.20: 8000"
    ]
    assert lines == expected, f"Content of {report_path} is incorrect. Expected {expected}, got {lines}."

def test_tls_certs():
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Key file {key_path} is missing."

    # Check valid RSA key
    result = subprocess.run(["openssl", "rsa", "-in", key_path, "-check", "-noout"], capture_output=True, text=True)
    assert result.returncode == 0, f"Invalid RSA key: {result.stderr}"

    # Check cert validity
    result = subprocess.run(["openssl", "x509", "-in", cert_path, "-noout", "-text"], capture_output=True, text=True)
    assert result.returncode == 0, f"Invalid certificate: {result.stderr}"
    assert "Signature Algorithm" in result.stdout, "Certificate does not appear to be a valid x509 cert."

def test_backup_script_functionality():
    script_path = "/home/user/backup_logs.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

    # Prepare a dummy log file to test the script
    log_path = "/home/user/app_logs/access.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w") as f:
        f.write("test log data for backup script\n")

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Backup script failed to execute. stderr: {result.stderr}"

    # Verify backup creation
    date_str = datetime.now().strftime("%Y-%m-%d")
    backup_path = f"/home/user/backup/access_{date_str}.log.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} was not created by the script."

    # Verify backup is valid gzip
    result = subprocess.run(["gzip", "-t", backup_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Backup file {backup_path} is not a valid gzip file."

    # Verify original log was emptied
    assert os.path.isfile(log_path), f"Original log file {log_path} was deleted instead of truncated."
    assert os.path.getsize(log_path) == 0, f"Original log file {log_path} was not truncated to zero bytes."

def test_crontab_scheduling():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Has it been configured?"

    lines = result.stdout.strip().split('\n')
    found = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Check for midnight execution and the script path
        if line.startswith("0 0 * * *") and "/home/user/backup_logs.sh" in line:
            found = True
            break

    assert found, "Crontab does not contain the correct scheduled task (0 0 * * * /home/user/backup_logs.sh)."