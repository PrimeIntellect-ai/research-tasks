# test_final_state.py

import os
import subprocess
import pytest

def test_libyaml_installed():
    lib_path = "/home/user/local/lib"
    assert os.path.isdir(lib_path), f"libyaml installation directory {lib_path} is missing."

    # Check if libyaml shared library exists
    files = os.listdir(lib_path)
    assert any("libyaml" in f for f in files), f"libyaml shared library not found in {lib_path}."

def test_validator_binary_exists():
    binary_path = "/home/user/manifest_validator"
    assert os.path.isfile(binary_path), f"Validator binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Validator binary {binary_path} is not executable."

def test_systemd_service_active():
    service_file = os.path.expanduser("~/.config/systemd/user/k8s-webhook.service")
    assert os.path.isfile(service_file), f"Systemd service file {service_file} is missing."

    # Check if service is active
    try:
        subprocess.run(
            ["systemctl", "--user", "is-active", "k8s-webhook.service"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"k8s-webhook.service is not active. systemctl output: {e.stdout} {e.stderr}")

def test_webhook_adversarial_corpus():
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".yaml") or f.endswith(".yml")]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".yaml") or f.endswith(".yml")]

    bypassed_evil = []
    modified_clean = []

    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        with open(filepath, "rb") as file_in:
            data = file_in.read()

        try:
            result = subprocess.run(
                ["socat", "-", "ssl:localhost:8443,verify=0"],
                input=data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            output = result.stdout.decode('utf-8').strip()
            if output != "REJECT":
                bypassed_evil.append(f)
        except Exception as e:
            bypassed_evil.append(f)

    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        with open(filepath, "rb") as file_in:
            data = file_in.read()

        try:
            result = subprocess.run(
                ["socat", "-", "ssl:localhost:8443,verify=0"],
                input=data,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            output = result.stdout.decode('utf-8').strip()
            if output != "ACCEPT":
                modified_clean.append(f)
        except Exception as e:
            modified_clean.append(f)

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))