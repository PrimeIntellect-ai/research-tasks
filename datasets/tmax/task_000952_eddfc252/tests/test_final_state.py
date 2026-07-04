# test_final_state.py

import os
import json
import pytest

def test_waf_tester_built():
    tester_path = "/app/go_waf/waf-tester"
    assert os.path.isfile(tester_path), f"Expected executable at {tester_path} is missing. Did you build the Go project?"
    assert os.access(tester_path, os.X_OK), f"File at {tester_path} is not executable."

def test_clean_corpus_results():
    clean_corpus_dir = "/app/corpora/clean/"
    results_file = "/app/clean_results.json"

    assert os.path.isfile(results_file), f"Expected results file at {results_file} is missing."

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON.")

    expected_files = {f for f in os.listdir(clean_corpus_dir) if f.endswith('.json')}

    modified_clean = []
    missing_clean = []

    for filename in expected_files:
        if filename not in results:
            missing_clean.append(filename)
        elif results[filename] != "CLEAN":
            modified_clean.append(filename)

    extra_files = set(results.keys()) - expected_files

    errors = []
    if missing_clean:
        errors.append(f"Missing {len(missing_clean)} files in results: {missing_clean}")
    if modified_clean:
        errors.append(f"{len(modified_clean)} of {len(expected_files)} clean modified (not mapped to CLEAN): {modified_clean}")
    if extra_files:
        errors.append(f"Unexpected files in results: {list(extra_files)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_evil_corpus_results():
    evil_corpus_dir = "/app/corpora/evil/"
    results_file = "/app/evil_results.json"

    assert os.path.isfile(results_file), f"Expected results file at {results_file} is missing."

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_file} is not valid JSON.")

    expected_files = {f for f in os.listdir(evil_corpus_dir) if f.endswith('.json')}

    bypassed_evil = []
    missing_evil = []

    for filename in expected_files:
        if filename not in results:
            missing_evil.append(filename)
        elif results[filename] != "EVIL":
            bypassed_evil.append(filename)

    extra_files = set(results.keys()) - expected_files

    errors = []
    if missing_evil:
        errors.append(f"Missing {len(missing_evil)} files in results: {missing_evil}")
    if bypassed_evil:
        errors.append(f"{len(bypassed_evil)} of {len(expected_files)} evil bypassed (not mapped to EVIL): {bypassed_evil}")
    if extra_files:
        errors.append(f"Unexpected files in results: {list(extra_files)}")

    if errors:
        pytest.fail(" | ".join(errors))