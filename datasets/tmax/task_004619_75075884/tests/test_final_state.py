# test_final_state.py
import os
import urllib.request
import urllib.error
import pytest

def test_status_file():
    path = "/home/user/status.txt"
    assert os.path.isfile(path), f"Status file missing at {path}"
    with open(path, "r") as f:
        content = f.read().strip()
    assert "DONE" in content, f"Status file does not contain DONE, got: {content}"

def test_clean_corpus():
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory at {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".json")]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_files = []

    for filepath in clean_files:
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request(
            "http://127.0.0.1:3030/validate", 
            data=data, 
            headers={"Content-Type": "application/json"}, 
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    failed_files.append((os.path.basename(filepath), response.status))
        except urllib.error.HTTPError as e:
            failed_files.append((os.path.basename(filepath), e.code))
        except Exception as e:
            failed_files.append((os.path.basename(filepath), str(e)))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected (expected 200 OK). Offending files: {failed_files}"

def test_evil_corpus():
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory at {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".json")]
    assert len(evil_files) > 0, "No evil corpus files found"

    bypassed_files = []

    for filepath in evil_files:
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request(
            "http://127.0.0.1:3030/validate", 
            data=data, 
            headers={"Content-Type": "application/json"}, 
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                # If it didn't raise HTTPError, it returned 2xx or 3xx. We expect 400.
                bypassed_files.append((os.path.basename(filepath), response.status))
        except urllib.error.HTTPError as e:
            if e.code != 400:
                bypassed_files.append((os.path.basename(filepath), e.code))
        except Exception as e:
            # Connection errors, timeouts, etc.
            bypassed_files.append((os.path.basename(filepath), str(e)))

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed or returned wrong status (expected 400 Bad Request). Offending files: {bypassed_files}"