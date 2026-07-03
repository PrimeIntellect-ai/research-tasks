# test_final_state.py

import os
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_filter_script_exists():
    assert os.path.isfile("/home/user/filter.py"), "/home/user/filter.py does not exist."

def test_corpora_validation():
    clean_dir = "/home/user/corpora/clean"
    evil_dir = "/home/user/corpora/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_modified = []
    for f in clean_files:
        res = subprocess.run(["python3", "/home/user/filter.py", f], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(f))

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run(["python3", "/home/user/filter.py", f], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    errors = []
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)

def test_end_to_end_flow():
    safe_path = "/home/user/docs_src/test_safe.md"
    evil_path = "/home/user/docs_src/test_evil.md"

    with open(safe_path, "w") as f:
        f.write("# Safe Document\nThis is a safe file.\n")

    with open(evil_path, "w") as f:
        f.write("# Evil Document\n!INCLUDE[/etc/shadow]\n")

    # Wait for the watcher and builder to process
    time.sleep(4)

    # Check safe file is served
    try:
        resp = urllib.request.urlopen("http://localhost:8080/test_safe.html")
        assert resp.status == 200, f"Expected safe file to be served with 200 OK, got {resp.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Safe file fetch failed with HTTP Error: {e.code}")
    except urllib.error.URLError as e:
        pytest.fail(f"Safe file fetch failed: {e.reason}")

    # Check evil file is NOT served
    try:
        resp = urllib.request.urlopen("http://localhost:8080/test_evil.html")
        pytest.fail("Evil file was served (200 OK) but should have been blocked (expected 404).")
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"Expected 404 for evil file, got {e.code}"
    except urllib.error.URLError as e:
        pass # Connection refused or similar is also acceptable if nginx drops it, but 404 is standard

    # Check quarantine log
    quarantine_log = "/home/user/quarantine.log"
    assert os.path.exists(quarantine_log), f"{quarantine_log} does not exist. Evil file was not logged."

    with open(quarantine_log, "r") as f:
        log_content = f.read()

    assert "test_evil.md" in log_content, "test_evil.md was not found in /home/user/quarantine.log."