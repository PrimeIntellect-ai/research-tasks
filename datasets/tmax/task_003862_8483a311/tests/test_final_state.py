# test_final_state.py

import os
import urllib.request
import ssl
import subprocess
import glob
import pytest

def test_tls_server_running_and_serving():
    """
    Verifies that the TLS server is running on port 8443, uses HTTPS,
    and serves the expected content at /index.html.
    """
    url = "https://127.0.0.1:8443/index.html"

    # Create an unverified SSL context to accept the self-signed certificate
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(url, context=ctx, timeout=5) as response:
            content = response.read().decode('utf-8').strip()
            assert content == "Deployment Node Active", \
                f"Expected index.html to contain 'Deployment Node Active', but got: '{content}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the TLS server at {url}. Is it running? Error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error while verifying TLS server: {e}")

def test_sanitizer_binary_exists():
    """
    Verifies that the compiled sanitizer binary exists and is executable.
    """
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"The sanitizer binary is missing at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"The sanitizer binary at {sanitizer_path} is not executable"

def test_sanitizer_adversarial_corpus():
    """
    Verifies the sanitizer against the clean and evil corpora.
    Clean files must return exit code 0.
    Evil files must return exit code 1 (or at least non-zero).
    """
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}"
    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}"

    clean_failures = []
    evil_bypasses = []

    # Test clean corpus
    for cf in clean_files:
        with open(cf, 'rb') as f:
            content = f.read()
        try:
            result = subprocess.run([sanitizer_path], input=content, capture_output=True, timeout=2)
            if result.returncode != 0:
                clean_failures.append(os.path.basename(cf))
        except Exception as e:
            pytest.fail(f"Execution of sanitizer failed on clean file {cf}: {e}")

    # Test evil corpus
    for ef in evil_files:
        with open(ef, 'rb') as f:
            content = f.read()
        try:
            result = subprocess.run([sanitizer_path], input=content, capture_output=True, timeout=2)
            # The spec requires exit code 1 for malicious files. We consider any 0 exit as a bypass.
            if result.returncode == 0:
                evil_bypasses.append(os.path.basename(ef))
        except Exception as e:
            pytest.fail(f"Execution of sanitizer failed on evil file {ef}: {e}")

    # Compile results
    error_messages = []
    if clean_failures:
        error_messages.append(
            f"{len(clean_failures)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_failures)}"
        )
    if evil_bypasses:
        error_messages.append(
            f"{len(evil_bypasses)} of {len(evil_files)} evil bypassed (accepted): {', '.join(evil_bypasses)}"
        )

    if error_messages:
        pytest.fail(" | ".join(error_messages))