# test_final_state.py

import os
import subprocess
import pytest

def test_waf_filter_binary_exists():
    binary_path = '/home/user/waf_filter'
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_gowaf_fixes():
    # Check parser.go
    parser_path = '/app/gowaf/parser.go'
    with open(parser_path, 'r') as f:
        parser_content = f.read()
    assert '"strings"' in parser_content, f"{parser_path} is still missing the 'strings' import."

    # Check Makefile
    makefile_path = '/app/gowaf/Makefile'
    with open(makefile_path, 'r') as f:
        makefile_content = f.read()
    assert 'go build' in makefile_content, f"{makefile_path} still has the typo or is missing 'go build'."
    assert 'go biuld' not in makefile_content, f"{makefile_path} still contains the 'go biuld' typo."

def test_adversarial_corpus_results():
    binary_path = '/home/user/waf_filter'
    evil_dir = '/home/user/corpus/evil/'
    clean_dir = '/home/user/corpus/clean/'

    # Run against evil corpus
    evil_result = subprocess.run([binary_path, evil_dir], capture_output=True, text=True)
    assert evil_result.returncode == 0, "waf_filter failed to run on evil corpus."
    evil_output = evil_result.stdout.strip().split('\n')
    evil_dict = {}
    for line in evil_output:
        if ': ' in line:
            fname, res = line.split(': ', 1)
            evil_dict[fname.strip()] = res.strip()

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    evil_bypassed = []
    for f in evil_files:
        if evil_dict.get(f) != 'EVIL':
            evil_bypassed.append(f)

    # Run against clean corpus
    clean_result = subprocess.run([binary_path, clean_dir], capture_output=True, text=True)
    assert clean_result.returncode == 0, "waf_filter failed to run on clean corpus."
    clean_output = clean_result.stdout.strip().split('\n')
    clean_dict = {}
    for line in clean_output:
        if ': ' in line:
            fname, res = line.split(': ', 1)
            clean_dict[fname.strip()] = res.strip()

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    clean_modified = []
    for f in clean_files:
        if clean_dict.get(f) != 'CLEAN':
            clean_modified.append(f)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msg, " | ".join(error_msg)