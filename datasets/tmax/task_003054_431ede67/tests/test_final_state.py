# test_final_state.py

import os
import subprocess

def test_analyze_malware_script_exists_and_executable():
    script_path = "/home/user/analyze_malware.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_extracted_cert_pem():
    cert_path = "/home/user/extracted_cert.pem"
    assert os.path.isfile(cert_path), f"File {cert_path} does not exist."

    # Check if it's a valid cert using openssl
    result = subprocess.run(['openssl', 'x509', '-in', cert_path, '-noout'], capture_output=True, text=True)
    assert result.returncode == 0, f"{cert_path} is not a valid certificate. OpenSSL error: {result.stderr}"

def test_cert_info_txt():
    info_path = "/home/user/cert_info.txt"
    assert os.path.isfile(info_path), f"File {info_path} does not exist."

    with open(info_path, 'r') as f:
        content = f.read()

    # Check for expected issuer and subject
    assert "issuer=" in content and "c2.evil-server.local" in content, "cert_info.txt does not contain the correct issuer information."
    assert "subject=" in content and "c2.evil-server.local" in content, "cert_info.txt does not contain the correct subject information."

def test_c2_url_txt():
    url_path = "/home/user/c2_url.txt"
    assert os.path.isfile(url_path), f"File {url_path} does not exist."

    with open(url_path, 'r') as f:
        content = f.read().strip()

    assert content == "https://c2.evil-server.local", f"Expected 'https://c2.evil-server.local' in {url_path}, but found '{content}'."