# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_build_artifacts_exist():
    assert os.path.isfile("/home/user/project/Makefile"), "Makefile is missing"
    assert os.path.isfile("/home/user/project/start.sh"), "start.sh is missing"
    assert os.path.isfile("/home/user/project/build/libsanitiser.so"), "libsanitiser.so was not built"
    assert os.path.isfile("/home/user/project/build/gateway"), "Go gateway executable was not built"

def test_adversarial_corpus():
    clean_dir = "/home/user/corpora/clean/"
    evil_dir = "/home/user/corpora/evil/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No clean corpus files found"
    assert len(evil_files) > 0, "No evil corpus files found"

    url = "http://127.0.0.1:8080/process"

    failed_clean = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request(url, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    failed_clean.append(filename)
        except urllib.error.HTTPError as e:
            failed_clean.append(filename)
        except Exception as e:
            failed_clean.append(f"{filename} (connection error: {e})")

    failed_evil = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request(url, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 403:
                    failed_evil.append(filename)
        except urllib.error.HTTPError as e:
            if e.code != 403:
                failed_evil.append(filename)
        except Exception as e:
            failed_evil.append(f"{filename} (connection error: {e})")

    error_messages = []
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified or rejected: {', '.join(failed_clean)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))