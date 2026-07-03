# test_final_state.py

import os
import subprocess
import pytest
import json

def test_video_event_result():
    path = "/home/user/video_event.txt"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "142-187", f"Incorrect frame range in {path}. Expected '142-187', got '{content}'"

def test_sanitizer_adversarial_corpus():
    sanitizer_src = "/home/user/sanitizer.go"
    assert os.path.isfile(sanitizer_src), f"Missing required file: {sanitizer_src}"

    sanitizer_bin = "/tmp/sanitizer"
    compile_cmd = ["go", "build", "-o", sanitizer_bin, sanitizer_src]
    compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Failed to compile {sanitizer_src}:\n{compile_res.stderr}"
    assert os.path.isfile(sanitizer_bin), f"Sanitizer binary not generated at {sanitizer_bin}"

    evil_corpus_dir = "/app/eval_corpus/evil"
    clean_corpus_dir = "/app/eval_corpus/clean"

    if not os.path.isdir(evil_corpus_dir):
        evil_corpus_dir = "/app/corpus/evil"
    if not os.path.isdir(clean_corpus_dir):
        clean_corpus_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_corpus_dir), f"Missing evil corpus directory: {evil_corpus_dir}"
    assert os.path.isdir(clean_corpus_dir), f"Missing clean corpus directory: {clean_corpus_dir}"

    evil_bypassed = []
    clean_modified = []

    for filename in os.listdir(evil_corpus_dir):
        filepath = os.path.join(evil_corpus_dir, filename)
        if not os.path.isfile(filepath):
            continue
        res = subprocess.run([sanitizer_bin, filepath])
        if res.returncode != 1:
            evil_bypassed.append(filename)

    for filename in os.listdir(clean_corpus_dir):
        filepath = os.path.join(clean_corpus_dir, filename)
        if not os.path.isfile(filepath):
            continue
        res = subprocess.run([sanitizer_bin, filepath])
        if res.returncode != 0:
            clean_modified.append(filename)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(os.listdir(evil_corpus_dir))} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(os.listdir(clean_corpus_dir))} clean modified/rejected: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)

def test_recover_go_exists():
    recover_src = "/home/user/recover.go"
    assert os.path.isfile(recover_src), f"Missing required file: {recover_src}"

    recovered_jsonl = "/home/user/recovered.jsonl"
    assert os.path.isfile(recovered_jsonl), f"Missing required file: {recovered_jsonl}"