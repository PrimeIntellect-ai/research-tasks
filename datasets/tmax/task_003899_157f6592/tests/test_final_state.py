# test_final_state.py
import os
import subprocess

def test_done_file():
    done_file = '/home/user/done.txt'
    assert os.path.isfile(done_file), f"Expected file {done_file} does not exist."
    with open(done_file, 'r') as f:
        content = f.read().strip()
    assert content == "READY", f"Expected {done_file} to contain 'READY', but found '{content}'."

def test_binary_exists_and_executable():
    binary_path = '/home/user/query_sanitizer'
    assert os.path.isfile(binary_path), f"Expected binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_adversarial_corpus():
    binary_path = '/home/user/query_sanitizer'
    evil_corpus_path = '/app/verifier/corpus/evil.txt'
    clean_corpus_path = '/app/verifier/corpus/clean.txt'

    assert os.path.isfile(evil_corpus_path), f"Evil corpus {evil_corpus_path} missing."
    assert os.path.isfile(clean_corpus_path), f"Clean corpus {clean_corpus_path} missing."

    # Process evil corpus
    with open(evil_corpus_path, 'r') as f:
        evil_queries = f.read().splitlines()

    evil_bypassed = []
    for query in evil_queries:
        if not query.strip():
            continue
        proc = subprocess.run([binary_path], input=query + '\n', text=True, capture_output=True)
        output = proc.stdout.strip()
        if output != "MALICIOUS":
            evil_bypassed.append(query)

    # Process clean corpus
    with open(clean_corpus_path, 'r') as f:
        clean_queries = f.read().splitlines()

    clean_modified = []
    for query in clean_queries:
        if not query.strip():
            continue
        proc = subprocess.run([binary_path], input=query + '\n', text=True, capture_output=True)
        output = proc.stdout.strip()
        if output != "SAFE":
            clean_modified.append(query)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_queries)} evil bypassed. Offending queries: {evil_bypassed[:5]}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_queries)} clean modified (flagged as malicious). Offending queries: {clean_modified[:5]}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msgs)