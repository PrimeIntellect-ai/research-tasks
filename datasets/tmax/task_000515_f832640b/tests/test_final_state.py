# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest

def test_json_header_fixed():
    json_hpp_path = "/app/json-3.11.2/single_include/nlohmann/json.hpp"
    assert os.path.isfile(json_hpp_path), f"File {json_hpp_path} does not exist."
    with open(json_hpp_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "#define std::size_t int" not in content, "The malicious macro '#define std::size_t int' is still present in json.hpp."

def test_binary_exists():
    binary_path = "/home/user/etl_filter"
    assert os.path.isfile(binary_path), f"Executable not found at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable."

def test_adversarial_corpus_filtering():
    binary_path = "/home/user/etl_filter"
    clean_corpus = "/app/data/clean/"
    evil_corpus = "/app/data/evil/"

    assert os.path.isdir(clean_corpus), "Clean corpus directory missing."
    assert os.path.isdir(evil_corpus), "Evil corpus directory missing."

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Execute the binary against both corpora
        try:
            subprocess.run([binary_path, clean_corpus, clean_out], check=True, capture_output=True, text=True)
            subprocess.run([binary_path, evil_corpus, evil_out], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Execution of {binary_path} failed.\nStdout: {e.stdout}\nStderr: {e.stderr}")

        # Validate clean corpus preservation
        clean_expected = set(f for f in os.listdir(clean_corpus) if f.endswith('.json'))
        clean_actual = set(os.listdir(clean_out))

        missing_clean = clean_expected - clean_actual
        modified_clean = []

        for f in clean_actual.intersection(clean_expected):
            with open(os.path.join(clean_corpus, f), "r") as src, open(os.path.join(clean_out, f), "r") as dst:
                try:
                    src_data = json.load(src)
                    dst_data = json.load(dst)
                    # Semantic equivalence check for JSON
                    if src_data != dst_data:
                        modified_clean.append(f)
                except json.JSONDecodeError:
                    modified_clean.append(f)

        # Validate evil corpus rejection
        evil_expected = set(f for f in os.listdir(evil_corpus) if f.endswith('.json'))
        evil_actual = set(os.listdir(evil_out))
        evil_bypassed = list(evil_actual)

        error_msgs = []
        if missing_clean or modified_clean:
            error_msgs.append(f"{len(missing_clean) + len(modified_clean)} of {len(clean_expected)} clean modified or rejected.")
            if missing_clean:
                error_msgs.append(f"Missing clean files: {', '.join(missing_clean)}.")
            if modified_clean:
                error_msgs.append(f"Modified clean files: {', '.join(modified_clean)}.")

        if evil_bypassed:
            error_msgs.append(f"{len(evil_bypassed)} of {len(evil_expected)} evil bypassed.")
            error_msgs.append(f"Bypassed evil files: {', '.join(evil_bypassed)}.")

        if error_msgs:
            pytest.fail(" ".join(error_msgs))