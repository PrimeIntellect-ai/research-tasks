# test_final_state.py
import os
import glob
import subprocess
import pytest

def test_tls_certificate_and_key():
    """Verify that the TLS certificate and private key exist and the key is encrypted with the correct passphrase."""
    key_path = "/home/user/audit_key.pem"
    cert_path = "/home/user/audit_cert.pem"

    assert os.path.exists(key_path), f"Missing private key at {key_path}"
    assert os.path.exists(cert_path), f"Missing certificate at {cert_path}"

    # Check if the key is encrypted with the correct passphrase derived from brute-forcing
    passphrase = "4829audit"
    cmd = ["openssl", "rsa", "-in", key_path, "-passin", f"pass:{passphrase}", "-check", "-noout"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"Private key is not encrypted with the correct passphrase or is invalid. OpenSSL stderr: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        pytest.fail("OpenSSL command timed out. The key might not be properly encrypted, causing OpenSSL to prompt for a password interactively.")

def test_classifier_corpus():
    """Verify that the classifier script correctly identifies clean and evil command invocations."""
    classifier_path = "/home/user/arg_classifier.py"
    assert os.path.exists(classifier_path), f"Missing classifier script at {classifier_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, "No clean corpus files found to test."
    assert len(evil_files) > 0, "No evil corpus files found to test."

    clean_failures = []
    for f in clean_files:
        cmd = ["python3", classifier_path, f]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "CLEAN":
                clean_failures.append(f"{os.path.basename(f)} (Output: {output})")
        except subprocess.TimeoutExpired:
            clean_failures.append(f"{os.path.basename(f)} (Timed out)")

    evil_failures = []
    for f in evil_files:
        cmd = ["python3", classifier_path, f]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            output = result.stdout.strip()
            if output != "EVIL":
                evil_failures.append(f"{os.path.basename(f)} (Output: {output})")
        except subprocess.TimeoutExpired:
            evil_failures.append(f"{os.path.basename(f)} (Timed out)")

    error_msg = ""
    if evil_failures:
        error_msg += f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}. "
    if clean_failures:
        error_msg += f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}."

    assert not evil_failures and not clean_failures, error_msg.strip()