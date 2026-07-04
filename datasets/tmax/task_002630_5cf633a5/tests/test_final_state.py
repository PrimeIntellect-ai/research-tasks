# test_final_state.py
import os
import glob
import urllib.request
import urllib.error
import pytest

APP_DIR = "/home/user/app"
CORPORA_DIR = os.path.join(APP_DIR, "corpora")
CLEAN_DIR = os.path.join(CORPORA_DIR, "clean")
EVIL_DIR = os.path.join(CORPORA_DIR, "evil")
SUCCESS_LOG = os.path.join(APP_DIR, "success.log")
EVAL_URL = "http://localhost:8080/eval"

def test_success_log_exists():
    assert os.path.isfile(SUCCESS_LOG), f"Expected success log at {SUCCESS_LOG} is missing."
    with open(SUCCESS_LOG, "r") as f:
        content = f.read()
    assert "READY" in content, f"Expected 'READY' in {SUCCESS_LOG}, but found: {content}"

def test_adversarial_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_DIR, "*.expr"))
    evil_files = glob.glob(os.path.join(EVIL_DIR, "*.expr"))

    assert len(clean_files) > 0, f"No clean corpus files found in {CLEAN_DIR}"
    assert len(evil_files) > 0, f"No evil corpus files found in {EVIL_DIR}"

    clean_failures = []
    for filepath in clean_files:
        basename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            data = f.read()
        req = urllib.request.Request(EVAL_URL, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    clean_failures.append(basename)
        except urllib.error.HTTPError as e:
            clean_failures.append(basename)
        except Exception as e:
            clean_failures.append(basename)

    evil_failures = []
    for filepath in evil_files:
        basename = os.path.basename(filepath)
        with open(filepath, "rb") as f:
            data = f.read()
        req = urllib.request.Request(EVAL_URL, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 400:
                    evil_failures.append(basename)
        except urllib.error.HTTPError as e:
            if e.code != 400:
                evil_failures.append(basename)
        except Exception as e:
            evil_failures.append(basename)

    error_msgs = []
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified (failed to return 200 OK): {', '.join(clean_failures)}")
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed (failed to return 400 Bad Request): {', '.join(evil_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))