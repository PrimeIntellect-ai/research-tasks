# test_final_state.py

import os
import stat
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_ssh_deploy_key():
    """Verify that the deploy_key exists."""
    key_path = "/home/user/.ssh/deploy_key"
    assert os.path.isfile(key_path), f"SSH key {key_path} was not created."

    # Also verify it's an ed25519 key by checking the public key or private key content
    with open(key_path, "r") as f:
        content = f.read()
    assert "OPENSSH PRIVATE KEY" in content, "deploy_key does not appear to be a valid OpenSSH private key."

def test_authorized_keys():
    """Verify that authorized_keys has the restricted deployment key."""
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"{auth_keys_path} does not exist."

    with open(auth_keys_path, "r") as f:
        content = f.read()

    expected_prefix = 'no-pty,no-port-forwarding,no-X11-forwarding,command="/home/user/run_sandboxed.sh" ssh-ed25519'
    assert expected_prefix in content, "authorized_keys does not contain the correct restrictions and key type."

def test_run_sandboxed_script():
    """Verify the sandboxed execution script."""
    script_path = "/home/user/run_sandboxed.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert content.startswith("#!/bin/bash"), "Script must start with #!/bin/bash shebang."

    expected_bwrap = "bwrap --ro-bind / / --dev /dev --unshare-all --share-net --bind /home/user/app /home/user/app /home/user/app/target/release/web_app"
    assert expected_bwrap in content, "Script does not contain the exact bwrap command required."

def test_rust_app_redirect():
    """Verify the compiled Rust application fixes the open redirect."""
    bin_path = "/home/user/app/target/release/web_app"
    assert os.path.isfile(bin_path), f"Compiled application not found at {bin_path}."

    # Start the application
    process = subprocess.Popen([bin_path])

    # Wait for the server to start
    time.sleep(2)

    try:
        # Helper to get redirect location
        def get_redirect_location(url):
            req = urllib.request.Request(url, method="GET")
            try:
                with urllib.request.urlopen(req) as response:
                    return response.geturl()
            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    return e.headers.get('Location')
                raise
            except urllib.error.URLError as e:
                # If redirect is invalid (e.g. just a path), urlopen might fail differently depending on python version
                # We can handle it by using a custom redirect handler
                pass

        # Better approach: use a custom opener that doesn't follow redirects
        class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None

        opener = urllib.request.build_opener(NoRedirectHandler)

        def fetch_location(path):
            url = f"http://127.0.0.1:8080{path}"
            req = urllib.request.Request(url)
            try:
                resp = opener.open(req)
                return resp.headers.get('Location')
            except urllib.error.HTTPError as e:
                return e.headers.get('Location')

        # Test normal redirect
        loc = fetch_location("/login?next=/profile")
        assert loc == "/profile", f"Expected redirect to /profile, got {loc}"

        # Test evil redirect (absolute URL)
        loc = fetch_location("/login?next=http://evil.com")
        assert loc == "/dashboard", f"Expected redirect to /dashboard for absolute URL, got {loc}"

        # Test protocol-relative redirect
        loc = fetch_location("/login?next=//evil.com")
        assert loc == "/dashboard", f"Expected redirect to /dashboard for protocol-relative URL, got {loc}"

        # Test missing next parameter
        loc = fetch_location("/login")
        assert loc == "/dashboard", f"Expected redirect to /dashboard for missing parameter, got {loc}"

    finally:
        process.terminate()
        process.wait()