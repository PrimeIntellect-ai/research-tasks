# test_final_state.py

import os
import urllib.request
import ssl
from difflib import SequenceMatcher

def test_expect_script_exists():
    """Check if the expect script was created."""
    path = "/home/user/automate.exp"
    assert os.path.isfile(path), f"Expect script {path} is missing."

def test_c_source_and_binary_exists():
    """Check if the C server source and compiled binary exist."""
    src_path = "/home/user/server.c"
    bin_path = "/home/user/server"
    assert os.path.isfile(src_path), f"C source file {src_path} is missing."
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

def test_certificates_exist():
    """Check if the self-signed certificates were generated."""
    cert_path = "/home/user/cert.pem"
    key_path = "/home/user/key.pem"
    assert os.path.isfile(cert_path), f"Certificate file {cert_path} is missing."
    assert os.path.isfile(key_path), f"Key file {key_path} is missing."

def test_transcript_served_over_https():
    """Fetch the transcript from the HTTPS server and verify its accuracy."""
    truth = "Alert system failure detected on node seven. Please restart the primary database daemon immediately."

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/"
    try:
        req = urllib.request.urlopen(url, context=ctx, timeout=5)
        result = req.read().decode('utf-8').strip()
    except Exception as e:
        assert False, f"Failed to fetch transcript from {url}: {e}"

    ratio = SequenceMatcher(None, truth.lower(), result.lower()).ratio()
    assert ratio >= 0.90, f"Transcript similarity ratio {ratio:.4f} is below the threshold of 0.90. Fetched: '{result}'"