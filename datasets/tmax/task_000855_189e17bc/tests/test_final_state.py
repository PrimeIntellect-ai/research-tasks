# test_final_state.py
import os
import subprocess
import hashlib
import re
import stat

def test_ssh_configuration():
    ssh_dir = "/home/user/.ssh"
    priv_key = os.path.join(ssh_dir, "id_ed25519")
    config_file = os.path.join(ssh_dir, "config")

    assert os.path.isfile(priv_key), f"SSH private key missing at {priv_key}"
    assert os.path.isfile(config_file), f"SSH config missing at {config_file}"

    with open(config_file, "r") as f:
        config_content = f.read()

    assert re.search(r"Host\s+\*", config_content, re.IGNORECASE), "SSH config missing 'Host *'"
    assert re.search(r"PasswordAuthentication\s+no", config_content, re.IGNORECASE), "SSH config missing 'PasswordAuthentication no'"

def test_clean_hashes():
    hash_file = "/home/user/clean_hashes.txt"
    assert os.path.isfile(hash_file), f"Missing {hash_file}"

    clean_dir = "/app/corpus/clean"
    expected_hashes = {}
    for filename in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, filename)
        if os.path.isfile(filepath):
            with open(filepath, "rb") as f:
                expected_hashes[filepath] = hashlib.sha256(f.read()).hexdigest()

    with open(hash_file, "r") as f:
        lines = f.readlines()

    parsed_hashes = {}
    for line in lines:
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            h, p = parts
            p = p.lstrip(" *")
            parsed_hashes[p] = h

    for filepath, expected_hash in expected_hashes.items():
        assert filepath in parsed_hashes or os.path.basename(filepath) in parsed_hashes, f"Missing hash for {filepath} in {hash_file}"
        actual_hash = parsed_hashes.get(filepath) or parsed_hashes.get(os.path.basename(filepath))
        assert actual_hash == expected_hash, f"Incorrect hash for {filepath}"

def test_redactor_script():
    script_path = "/home/user/redactor.py"
    assert os.path.isfile(script_path), f"Missing redactor script at {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"
    malicious_domain = "malicious-redirect-host.local"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failures = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "r") as f:
            original_content = f.read()

        result = subprocess.run([script_path, filepath], capture_output=True, text=True)
        if result.returncode != 0 or result.stdout != original_content:
            clean_failures.append(filename)

    evil_failures = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run([script_path, filepath], capture_output=True, text=True)

        if result.returncode != 0:
            evil_failures.append(filename)
            continue

        output = result.stdout

        # Check if malicious domain is redacted
        if malicious_domain in output:
            evil_failures.append(filename)
            continue

        # Check if private key block is redacted
        if "PRIVATE KEY-----" in output:
            evil_failures.append(filename)
            continue

    error_msg = []
    if evil_failures:
        error_msg.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msg.append(f"{len(clean_failures)} of {len(clean_files)} clean modified: {', '.join(clean_failures)}")

    assert not error_msg, " | ".join(error_msg)