# test_final_state.py

import os
import subprocess
import pytest
from datetime import datetime

def test_rogue_cn_extracted():
    """Verify that the rogue CN was correctly extracted from the video."""
    cn_file = "/home/user/rogue_cn.txt"
    assert os.path.isfile(cn_file), f"Missing rogue CN file: {cn_file}"

    with open(cn_file, "r") as f:
        cn_value = f.read().strip()

    expected_cn = "c2-backend.corp.attacker.net"
    assert cn_value == expected_cn, f"Incorrect rogue CN. Expected '{expected_cn}', got '{cn_value}'"

def test_detector_script_against_corpus():
    """Verify the detector script classifies all corpus files correctly."""
    detector_script = "/home/user/detector.py"
    assert os.path.isfile(detector_script), f"Missing detector script: {detector_script}"

    evil_corpus = "/app/corpus/evil/"
    clean_corpus = "/app/corpus/clean/"

    evil_files = [os.path.join(evil_corpus, f) for f in os.listdir(evil_corpus) if os.path.isfile(os.path.join(evil_corpus, f))]
    clean_files = [os.path.join(clean_corpus, f) for f in os.listdir(clean_corpus) if os.path.isfile(os.path.join(clean_corpus, f))]

    evil_bypassed = []
    clean_modified = []

    for filepath in evil_files:
        try:
            result = subprocess.run(["python3", detector_script, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "EVIL":
                evil_bypassed.append(os.path.basename(filepath))
        except Exception:
            evil_bypassed.append(os.path.basename(filepath))

    for filepath in clean_files:
        try:
            result = subprocess.run(["python3", detector_script, filepath], capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_modified.append(os.path.basename(filepath))
        except Exception:
            clean_modified.append(os.path.basename(filepath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {clean_modified}")

    assert not error_msgs, " | ".join(error_msgs)

def test_credential_rotation():
    """Verify the newly generated credentials."""
    key_file = "/home/user/new_key.pem"
    cert_file = "/home/user/new_cert.pem"

    assert os.path.isfile(key_file), f"Missing private key: {key_file}"
    assert os.path.isfile(cert_file), f"Missing certificate: {cert_file}"

    # Check if key is RSA
    key_check = subprocess.run(["openssl", "rsa", "-in", key_file, "-check", "-noout"], capture_output=True, text=True)
    assert key_check.returncode == 0, "new_key.pem is not a valid RSA private key"

    # Check certificate subject
    cert_subj = subprocess.run(["openssl", "x509", "-in", cert_file, "-noout", "-subject"], capture_output=True, text=True)
    assert cert_subj.returncode == 0, "new_cert.pem is not a valid certificate"
    assert "CN = legit-update.local" in cert_subj.stdout or "CN=legit-update.local" in cert_subj.stdout, "Certificate does not have the correct Subject CN"

    # Check certificate validity dates
    cert_dates = subprocess.run(["openssl", "x509", "-in", cert_file, "-noout", "-dates"], capture_output=True, text=True)
    assert cert_dates.returncode == 0, "Failed to read certificate dates"

    dates = {}
    for line in cert_dates.stdout.strip().split('\n'):
        if '=' in line:
            key, val = line.split('=', 1)
            dates[key] = val

    assert "notBefore" in dates and "notAfter" in dates, "Certificate dates missing"

    not_before = datetime.strptime(dates["notBefore"], "%b %d %H:%M:%S %Y %Z")
    not_after = datetime.strptime(dates["notAfter"], "%b %d %H:%M:%S %Y %Z")

    diff_days = (not_after - not_before).days
    assert diff_days == 365, f"Certificate validity is {diff_days} days, expected 365 days"