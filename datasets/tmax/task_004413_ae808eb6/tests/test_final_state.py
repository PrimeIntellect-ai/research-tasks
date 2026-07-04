# test_final_state.py

import os
import json
import pytest

CLEAN_CORPUS_DIR = "/home/user/tests/corpora/clean/"
EVIL_CORPUS_DIR = "/home/user/tests/corpora/evil/"
CLEAN_JSONL_PATH = "/home/user/etl_output/clean.jsonl"
REJECTED_JSONL_PATH = "/home/user/etl_output/rejected.jsonl"

def load_jsonl(path):
    if not os.path.exists(path):
        return {}
    res = {}
    with open(path, 'r') as f:
        for line in f:
            if not line.strip(): 
                continue
            try:
                data = json.loads(line)
                if 'transaction_id' in data:
                    res[data['transaction_id']] = data
            except json.JSONDecodeError:
                pass
    return res

def test_output_directories_and_files_exist():
    assert os.path.isdir("/home/user/etl_output/"), "The directory /home/user/etl_output/ was not created."
    assert os.path.isfile(CLEAN_JSONL_PATH) or os.path.isfile(REJECTED_JSONL_PATH), "Neither clean.jsonl nor rejected.jsonl were created."

def test_clean_corpus_accepted():
    clean_jsonl = load_jsonl(CLEAN_JSONL_PATH)

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.json')]
    assert len(clean_files) > 0, "No clean corpus files found to test."

    bypassed = []
    for fname in clean_files:
        with open(os.path.join(CLEAN_CORPUS_DIR, fname), 'r') as f:
            data = json.load(f)

        tid = data.get('transaction_id')
        if tid not in clean_jsonl:
            bypassed.append(fname)

    assert not bypassed, f"{len(bypassed)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(bypassed)}"

def test_evil_corpus_rejected():
    rejected_jsonl = load_jsonl(REJECTED_JSONL_PATH)

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.json')]
    assert len(evil_files) > 0, "No evil corpus files found to test."

    bypassed = []
    for fname in evil_files:
        with open(os.path.join(EVIL_CORPUS_DIR, fname), 'r') as f:
            data = json.load(f)

        tid = data.get('transaction_id')
        if tid not in rejected_jsonl:
            bypassed.append(fname)

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}"