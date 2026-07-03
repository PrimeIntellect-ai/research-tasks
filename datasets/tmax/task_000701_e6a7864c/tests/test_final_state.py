# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_nginx_proxy_works():
    """
    Test that the nginx proxy is correctly routing to the flask app.
    We expect a 302 redirect and a Set-Cookie header.
    """
    url = "http://127.0.0.1:8080/auth?next=/settings"

    # We use a custom opener to catch the 302 without automatically following it
    class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirectHandler)

    try:
        response = opener.open(url, timeout=5)
        status = response.getcode()
        headers = response.info()
    except urllib.error.HTTPError as e:
        status = e.code
        headers = e.headers
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to nginx on port 8080. Is it running? Error: {e}")

    assert status == 302, f"Expected HTTP 302 redirect, but got {status}"

    set_cookie = headers.get("Set-Cookie", "")
    assert "auth_token=" in set_cookie, "Expected 'Set-Cookie: auth_token=' in the response headers."

def test_token_validator_compiled():
    """
    Check that the token validator has been compiled.
    """
    binary_path = "/home/user/token_validator"
    assert os.path.isfile(binary_path), f"The compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_token_validator_clean_corpus():
    """
    Check that the token validator accepts all clean tokens.
    """
    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "rb") as f:
            result = subprocess.run(
                ["/home/user/token_validator"],
                stdin=f,
                capture_output=True,
                text=True
            )

        output = result.stdout.strip()
        if result.returncode != 0 or output != "VALID":
            failed_files.append((filename, result.returncode, output))

    if failed_files:
        details = ", ".join([f"{name} (code={code}, out='{out}')" for name, code, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean tokens modified/rejected: {details}")

def test_token_validator_evil_corpus():
    """
    Check that the token validator rejects all evil tokens.
    """
    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "rb") as f:
            result = subprocess.run(
                ["/home/user/token_validator"],
                stdin=f,
                capture_output=True,
                text=True
            )

        output = result.stdout.strip()
        if result.returncode != 1 or output != "INVALID":
            failed_files.append((filename, result.returncode, output))

    if failed_files:
        details = ", ".join([f"{name} (code={code}, out='{out}')" for name, code, out in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil tokens bypassed: {details}")