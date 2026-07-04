# test_final_state.py

import os
import glob
import urllib.request
import urllib.error
import pytest

def test_evil_corpus_rejected():
    """
    Iterate over every file in the evil corpus path declared by truth
    and assert the agent's solution rejects each one (returns HTTP 400).
    """
    evil_files = glob.glob("/app/data/evil/*.txt")
    assert len(evil_files) == 50, f"Expected 50 evil files, found {len(evil_files)}"

    bypassed = []
    for filepath in evil_files:
        with open(filepath, 'rb') as f:
            data = f.read()

        req = urllib.request.Request("http://127.0.0.1:8000/api/process", data=data, method="POST")
        try:
            response = urllib.request.urlopen(req, timeout=5)
            status = response.getcode()
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:
            status = str(e)

        if status != 400:
            bypassed.append(os.path.basename(filepath))

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed (did not return 400): {', '.join(bypassed[:10])}"

def test_clean_corpus_accepted():
    """
    Iterate over every file in the clean corpus path declared by truth
    and assert the agent's solution preserves/accepts each one (returns HTTP 200).
    """
    clean_files = glob.glob("/app/data/clean/*.txt")
    assert len(clean_files) == 50, f"Expected 50 clean files, found {len(clean_files)}"

    modified = []
    for filepath in clean_files:
        with open(filepath, 'rb') as f:
            data = f.read()

        req = urllib.request.Request("http://127.0.0.1:8000/api/process", data=data, method="POST")
        try:
            response = urllib.request.urlopen(req, timeout=5)
            status = response.getcode()
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:
            status = str(e)

        if status != 200:
            modified.append(os.path.basename(filepath))

    assert not modified, f"{len(modified)} of {len(clean_files)} clean modified (did not return 200): {', '.join(modified[:10])}"