# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import pytest

EVIL_DIR = "/home/user/app/corpora/evil/"
CLEAN_DIR = "/home/user/app/corpora/clean/"
ENDPOINT = "http://127.0.0.1:8080/validate"

def post_json(url, data):
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return None, None

def test_adversarial_corpus():
    if not os.path.isdir(EVIL_DIR) or not os.path.isdir(CLEAN_DIR):
        pytest.fail("Corpus directories are missing.")

    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.json')]
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.json')]

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        with open(os.path.join(EVIL_DIR, f), 'r') as fp:
            data = json.load(fp)
        status, _ = post_json(ENDPOINT, data)
        if status != 400:
            evil_bypassed.append(f)

    for f in clean_files:
        with open(os.path.join(CLEAN_DIR, f), 'r') as fp:
            data = json.load(fp)
        status, _ = post_json(ENDPOINT, data)
        if status != 200:
            clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))