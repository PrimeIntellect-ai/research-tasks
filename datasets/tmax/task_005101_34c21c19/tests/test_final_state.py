# test_final_state.py

import os
import json
import urllib.request
import pytest

def classify_sequence(sequence):
    url = "http://127.0.0.1:5000/classify"
    data = json.dumps({"sequence": sequence}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("status")
    except Exception as e:
        return f"error: {str(e)}"

def test_adversarial_corpus_evaluation():
    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_dir), f"Directory {evil_dir} does not exist"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist"

    evil_files = sorted([f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))])
    clean_files = sorted([f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))])

    assert len(evil_files) > 0, "No files found in evil corpus"
    assert len(clean_files) > 0, "No files found in clean corpus"

    bypassed_evil = []
    for filename in evil_files:
        with open(os.path.join(evil_dir, filename), "r") as f:
            sequence = f.read().strip()
        status = classify_sequence(sequence)
        if status != "evil":
            bypassed_evil.append(filename)

    modified_clean = []
    for filename in clean_files:
        with open(os.path.join(clean_dir, filename), "r") as f:
            sequence = f.read().strip()
        status = classify_sequence(sequence)
        if status != "clean":
            modified_clean.append(filename)

    errors = []
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {bypassed_evil}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {modified_clean}")

    if errors:
        pytest.fail(" | ".join(errors))