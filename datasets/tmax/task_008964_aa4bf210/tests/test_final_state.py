# test_final_state.py

import os
import re
import pytest

def test_certs_exist():
    cert_path = "/home/user/service/certs/cert.pem"
    key_path = "/home/user/service/certs/key.pem"

    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Private key file {key_path} is missing."

def test_go_code_fixed():
    go_file = "/home/user/service/backup_daemon.go"
    assert os.path.isfile(go_file), f"File {go_file} does not exist."

    with open(go_file, "r") as f:
        content = f.read()

    assert "ListenAndServeTLS" in content, "The Go file does not use ListenAndServeTLS as required for HTTPS."
    assert '":8443"' in content, "The Go file is not configured to listen on port 8443."

def test_tunnel_cmd():
    cmd_file = "/home/user/tunnel_cmd.sh"
    assert os.path.isfile(cmd_file), f"File {cmd_file} does not exist."

    with open(cmd_file, "r") as f:
        content = f.read().strip()

    assert content.startswith("ssh") or " ssh " in content, "The command does not appear to be an SSH command."
    assert "-L" in content, "The SSH command is missing the -L flag for local port forwarding."

    # Check for the port forwarding mapping
    mapping_pattern = r"9443:(localhost|127\.0\.0\.1):8443"
    assert re.search(mapping_pattern, content), "The SSH command does not correctly forward local port 9443 to localhost:8443."

    assert "user@localhost" in content, "The SSH command does not specify the correct user@localhost destination."

def test_restored_data():
    orig_secrets = "/home/user/important_data/secrets.env"
    restored_secrets = "/home/user/restored_data/secrets.env"

    orig_customers = "/home/user/important_data/customers.csv"
    restored_customers = "/home/user/restored_data/customers.csv"

    assert os.path.isfile(restored_secrets), f"Restored file {restored_secrets} is missing."
    assert os.path.isfile(restored_customers), f"Restored file {restored_customers} is missing."

    with open(orig_secrets, "r") as f:
        expected_secrets = f.read()
    with open(restored_secrets, "r") as f:
        actual_secrets = f.read()

    assert actual_secrets == expected_secrets, "The restored secrets.env does not match the original."

    with open(orig_customers, "r") as f:
        expected_customers = f.read()
    with open(restored_customers, "r") as f:
        actual_customers = f.read()

    assert actual_customers == expected_customers, "The restored customers.csv does not match the original."

def test_backup_archive_exists():
    archive_path = "/home/user/backup_verified.tar.gz"
    assert os.path.isfile(archive_path), f"The downloaded backup archive {archive_path} is missing."