# test_final_state.py
import os
import json
import glob
import subprocess
import urllib.request
import urllib.error
import pytest

EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
URL = "http://127.0.0.1:8000/api/v2/migrate"
LEGACY_BINARY = "/app/migrator_legacy"

def send_post(url, data):
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except urllib.error.URLError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)

def get_legacy_output(data):
    result = subprocess.run([LEGACY_BINARY], input=data, capture_output=True, timeout=5)
    if result.returncode != 0:
        return None
    return result.stdout.decode('utf-8')

def test_server_running():
    status, body = send_post(URL, b'{}')
    assert status is not None, f"Server is not reachable or failed to respond at {URL}. Error: {body}"

def test_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.json"))
    assert evil_files, f"No files found in {EVIL_CORPUS_DIR}"

    bypassed = []

    for file_path in sorted(evil_files):
        with open(file_path, 'rb') as f:
            data = f.read()

        status, body = send_post(URL, data)
        if status != 403 or body.strip() != "REJECTED":
            bypassed.append(os.path.basename(file_path))

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.json"))
    assert clean_files, f"No files found in {CLEAN_CORPUS_DIR}"

    modified = []

    for file_path in sorted(clean_files):
        with open(file_path, 'rb') as f:
            data = f.read()

        expected_output_raw = get_legacy_output(data)
        assert expected_output_raw is not None, f"Legacy binary failed on {file_path}"

        expected_json = json.loads(expected_output_raw)

        status, body = send_post(URL, data)
        if status != 200:
            modified.append(os.path.basename(file_path))
            continue

        try:
            actual_json = json.loads(body)
            if actual_json != expected_json:
                modified.append(os.path.basename(file_path))
        except json.JSONDecodeError:
            modified.append(os.path.basename(file_path))

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified. Offending files: {', '.join(modified)}")