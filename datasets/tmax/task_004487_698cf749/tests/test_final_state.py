# test_final_state.py

import os
import glob
import urllib.request
import urllib.error
import pytest

CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
API_URL = "http://127.0.0.1:8000/validate-patch"

def test_api_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.diff"))
    assert clean_files, "Clean corpus files missing"

    failed_files = []

    for filepath in clean_files:
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={"Content-Type": "text/plain"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    failed_files.append((os.path.basename(filepath), response.status))
        except urllib.error.HTTPError as e:
            failed_files.append((os.path.basename(filepath), e.code))
        except urllib.error.URLError as e:
            pytest.fail(f"Could not connect to API: {e.reason}")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files rejected: {failed_files}")

def test_api_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.diff"))
    assert evil_files, "Evil corpus files missing"

    failed_files = []

    for filepath in evil_files:
        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={"Content-Type": "text/plain"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 403:
                    failed_files.append((os.path.basename(filepath), response.status))
        except urllib.error.HTTPError as e:
            if e.code != 403:
                failed_files.append((os.path.basename(filepath), e.code))
        except urllib.error.URLError as e:
            pytest.fail(f"Could not connect to API: {e.reason}")

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {failed_files}")