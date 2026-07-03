# test_final_state.py

import os
import subprocess
import pytest
import re

def test_nginx_proxy_configured():
    nginx_conf = "/etc/nginx/sites-available/default"
    assert os.path.isfile(nginx_conf), f"Nginx config not found at {nginx_conf}"
    with open(nginx_conf, "r") as f:
        content = f.read()
    assert "proxy_pass" in content and "5000" in content, "Nginx is not configured to proxy to port 5000"

def test_flask_app_modifications():
    app_py = "/app/flask/app.py"
    assert os.path.isfile(app_py), f"Flask app not found at {app_py}"
    with open(app_py, "r") as f:
        content = f.read()
    assert "redteam_hunter_99" in content, "JWT secret 'redteam_hunter_99' not found in app.py"
    assert "paramiko" in content or "pysftp" in content or "sftp" in content.lower(), "SFTP logic not found in app.py"

def test_ssh_key_generated():
    priv_key = "/home/flask_svc/.ssh/id_rsa"
    pub_key = "/home/flask_svc/.ssh/id_rsa.pub"
    auth_keys = "/home/flask_svc/.ssh/authorized_keys"

    # We just check if the files exist, assuming flask_svc user's home is /home/flask_svc
    # If the user created them elsewhere or with different names, this might fail, but standard is id_rsa
    if os.path.exists("/home/flask_svc"):
        assert os.path.isfile(priv_key), f"SSH private key not found at {priv_key}"
        assert os.path.isfile(auth_keys), f"authorized_keys not found at {auth_keys}"

def test_firewall_rules_saved():
    rules_file = "/home/user/firewall_rules.v4"
    assert os.path.isfile(rules_file), f"Firewall rules not saved to {rules_file}"
    with open(rules_file, "r") as f:
        content = f.read()
    # Basic checks for ports
    assert "8080" in content, "Port 8080 not found in firewall rules"
    assert "5000" in content, "Port 5000 not found in firewall rules"
    assert "2222" in content, "Port 2222 not found in firewall rules"
    assert "DROP" in content or "REJECT" in content, "No DROP/REJECT policy found in firewall rules"

def test_sanitizer_adversarial_corpus():
    sanitizer_script = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_script), f"Sanitizer script not found at {sanitizer_script}"

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_bypassed = []
    evil_total = 0

    for filename in os.listdir(evil_dir):
        filepath = os.path.join(evil_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "r") as f:
            payloads = f.read().splitlines()

        for payload in payloads:
            if not payload.strip():
                continue
            evil_total += 1
            result = subprocess.run(
                ["python3", sanitizer_script, "--filename", payload.strip(), "--path", "/tmp"],
                capture_output=True,
                text=True
            )
            if "EVIL" not in result.stdout:
                evil_bypassed.append(payload.strip())

    clean_modified = []
    clean_total = 0

    for filename in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, "r") as f:
            payloads = f.read().splitlines()

        for payload in payloads:
            if not payload.strip():
                continue
            clean_total += 1
            result = subprocess.run(
                ["python3", sanitizer_script, "--filename", payload.strip(), "--path", "/tmp"],
                capture_output=True,
                text=True
            )
            if "SAFE" not in result.stdout:
                clean_modified.append(payload.strip())

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {evil_total} evil bypassed. Offending payloads: {evil_bypassed[:5]}...")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {clean_total} clean modified/rejected. Offending payloads: {clean_modified[:5]}...")

    assert not error_msgs, " | ".join(error_msgs)