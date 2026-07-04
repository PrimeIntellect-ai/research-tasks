# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_clean_corpus():
    """Verify that all clean payloads pass through the WAF and return 200 OK."""
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed = []

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'r') as f:
            data = f.read().encode('utf-8')

        req = urllib.request.Request(
            "http://127.0.0.1:8000/build", 
            data=data, 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    failed.append(f"{filename} (status {response.status})")
        except urllib.error.HTTPError as e:
            failed.append(f"{filename} (HTTPError {e.code})")
        except Exception as e:
            failed.append(f"{filename} (Exception {e})")

    assert not failed, f"{len(failed)} of {len(clean_files)} clean modified/blocked: {', '.join(failed)}"

def test_evil_corpus():
    """Verify that all evil payloads are blocked by the WAF and return 403 Forbidden."""
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Directory {evil_dir} does not exist"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found"

    failed = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r') as f:
            data = f.read().encode('utf-8')

        req = urllib.request.Request(
            "http://127.0.0.1:8000/build", 
            data=data, 
            headers={'Content-Type': 'application/json'}, 
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 403:
                    failed.append(f"{filename} (status {response.status})")
        except urllib.error.HTTPError as e:
            if e.code != 403:
                failed.append(f"{filename} (HTTPError {e.code})")
        except Exception as e:
            failed.append(f"{filename} (Exception {e})")

    assert not failed, f"{len(failed)} of {len(evil_files)} evil bypassed: {', '.join(failed)}"