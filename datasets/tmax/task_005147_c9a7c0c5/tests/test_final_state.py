# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_classifier_script_exists_and_executable():
    script_path = "/home/user/classifier.sh"
    assert os.path.isfile(script_path), f"Classifier script not found at {script_path}."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Classifier script at {script_path} is not executable."

def test_adversarial_corpus():
    script_path = "/home/user/classifier.sh"
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    failed_clean = []
    for cf in clean_files:
        result = subprocess.run([script_path, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True)
        if result.returncode != 1:
            failed_evil.append(os.path.basename(ef))

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed/accepted: {', '.join(failed_evil)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_network_interface_waf0():
    try:
        result = subprocess.run(["ip", "addr", "show", "waf0"], capture_output=True, text=True, check=True)
        output = result.stdout
        assert "10.100.0.1/24" in output or "10.100.0.1" in output, "waf0 interface exists but does not have the expected IP address 10.100.0.1/24."
    except subprocess.CalledProcessError:
        pytest.fail("Network interface 'waf0' does not exist or 'ip' command failed.")

def test_tls_certificates():
    crt_path = "/home/user/certs/tls.crt"
    key_path = "/home/user/certs/tls.key"

    assert os.path.isfile(crt_path), f"TLS certificate missing at {crt_path}."
    assert os.path.isfile(key_path), f"TLS private key missing at {key_path}."

    # Check if crt is a valid x509 cert
    crt_check = subprocess.run(["openssl", "x509", "-in", crt_path, "-noout"], capture_output=True)
    assert crt_check.returncode == 0, f"File at {crt_path} is not a valid x509 certificate."

    # Check if key is a valid private key (try rsa first, then ec, or just check if openssl pkey can parse it)
    key_check = subprocess.run(["openssl", "pkey", "-in", key_path, "-noout"], capture_output=True)
    assert key_check.returncode == 0, f"File at {key_path} is not a valid private key."