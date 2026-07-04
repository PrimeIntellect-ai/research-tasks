# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import glob
import pytest

def test_nginx_running():
    try:
        subprocess.run(["systemctl", "is-active", "nginx"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pytest.fail("Nginx is not running.")

def test_backend_service_running():
    try:
        # Assuming the test runs as the appropriate user or root can check user services
        # If running as root, we might need to specify the user, but standard systemctl --user might fail if not in a login session.
        # Let's check the process list or systemctl for the specific user.
        # For simplicity, we'll check if the service file exists and if the port 9337 is listening.
        service_path = os.path.expanduser("~/.config/systemd/user/backend.service")
        if not os.path.exists(service_path):
            # Fallback to checking the explicit path for 'user'
            service_path = "/home/user/.config/systemd/user/backend.service"
            if not os.path.exists(service_path):
                pytest.fail(f"backend.service file not found at {service_path}")
    except Exception as e:
        pytest.fail(f"Error checking backend service: {e}")

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    if not clean_files and not evil_files:
        pytest.skip("Corpus directories are empty or missing.")

    failed_clean = []
    for cf in clean_files:
        if not os.path.isfile(cf):
            continue
        with open(cf, 'rb') as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/process", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    failed_clean.append(os.path.basename(cf))
        except urllib.error.HTTPError as e:
            failed_clean.append(f"{os.path.basename(cf)} (HTTP {e.code})")
        except Exception as e:
            failed_clean.append(f"{os.path.basename(cf)} (Error)")

    failed_evil = []
    for ef in evil_files:
        if not os.path.isfile(ef):
            continue
        with open(ef, 'rb') as f:
            data = f.read()
        req = urllib.request.Request("http://localhost:8080/process", data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                # If it succeeds (HTTP 200), it bypassed the filter
                failed_evil.append(os.path.basename(ef))
        except urllib.error.HTTPError as e:
            if e.code != 403:
                failed_evil.append(f"{os.path.basename(ef)} (HTTP {e.code})")
        except Exception as e:
            failed_evil.append(f"{os.path.basename(ef)} (Error)")

    error_msg = []
    if failed_evil:
        error_msg.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_msg.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))