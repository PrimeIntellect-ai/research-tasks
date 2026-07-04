# test_final_state.py
import os
import time
import subprocess
import urllib.request
import urllib.error
import glob
import pytest

def wait_for_server():
    for _ in range(15):
        try:
            # Just test if the port is open and accepting HTTP requests
            req = urllib.request.Request("http://localhost:8080/", method="GET")
            urllib.request.urlopen(req, timeout=1)
            return True
        except urllib.error.HTTPError:
            # Any HTTP error means the server is responding to HTTP
            return True
        except Exception:
            time.sleep(1)
    return False

def test_server_running_and_corpora_validation():
    # If not running, try starting
    if not wait_for_server():
        start_script = "/home/user/start.sh"
        if os.path.exists(start_script):
            subprocess.Popen(["bash", start_script])
            assert wait_for_server(), "Server did not start on port 8080 after running start.sh"
        else:
            pytest.fail("Server is not running on port 8080 and /home/user/start.sh does not exist.")

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.mab"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.mab"))

    assert clean_files, f"No clean files found in {clean_dir}"
    assert evil_files, f"No evil files found in {evil_dir}"

    failed_clean = []
    for f in clean_files:
        with open(f, "rb") as fp:
            data = fp.read()
        req = urllib.request.Request("http://localhost:8080/validate", data=data, method="POST")
        try:
            resp = urllib.request.urlopen(req, timeout=5)
            if resp.status != 200:
                failed_clean.append((os.path.basename(f), resp.status))
        except urllib.error.HTTPError as e:
            failed_clean.append((os.path.basename(f), e.code))
        except Exception as e:
            failed_clean.append((os.path.basename(f), str(e)))

    failed_evil = []
    for f in evil_files:
        with open(f, "rb") as fp:
            data = fp.read()
        req = urllib.request.Request("http://localhost:8080/validate", data=data, method="POST")
        try:
            resp = urllib.request.urlopen(req, timeout=5)
            # If it succeeds or returns something other than 4xx, it's a failure
            if resp.status < 400 or resp.status >= 500:
                failed_evil.append((os.path.basename(f), resp.status))
        except urllib.error.HTTPError as e:
            # We want a 4xx error
            if e.code < 400 or e.code >= 500:
                failed_evil.append((os.path.basename(f), e.code))
        except Exception as e:
            # Network errors or timeouts
            failed_evil.append((os.path.basename(f), str(e)))

    errors = []
    if failed_clean:
        errors.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {failed_clean}")
    if failed_evil:
        errors.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {failed_evil}")

    if errors:
        pytest.fail("\n".join(errors))