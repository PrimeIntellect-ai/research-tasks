# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

CLEAN_CORPUS_DIR = "/home/user/corpus/clean"
EVIL_CORPUS_DIR = "/home/user/corpus/evil"
TARGET_URL = "http://127.0.0.1:8080/api/patch"

def send_post_request(url, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return None

def test_adversarial_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    clean_failed = []
    evil_bypassed = []

    for filename in clean_files:
        filepath = os.path.join(CLEAN_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            payload = json.load(f)
        status = send_post_request(TARGET_URL, payload)
        if status != 200:
            clean_failed.append(f"{filename} (status: {status})")

    for filename in evil_files:
        filepath = os.path.join(EVIL_CORPUS_DIR, filename)
        with open(filepath, 'r') as f:
            payload = json.load(f)
        status = send_post_request(TARGET_URL, payload)
        if status != 403:
            evil_bypassed.append(f"{filename} (status: {status})")

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    if errors:
        pytest.fail(" | ".join(errors))