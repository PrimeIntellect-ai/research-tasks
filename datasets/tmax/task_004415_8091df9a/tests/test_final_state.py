# test_final_state.py

import os
import sys
import importlib.util
import pytest

def test_nginx_conf_fixed():
    path = "/app/services/nginx.conf"
    assert os.path.isfile(path), f"Missing nginx configuration at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:5000;" in content, "nginx.conf was not updated to route to port 5000"
    assert "proxy_pass http://127.0.0.1:5001;" not in content, "nginx.conf still contains the misconfigured port 5001"

def test_adversarial_corpus_filter():
    filter_path = "/home/user/filter.py"
    assert os.path.isfile(filter_path), f"Missing filter module at {filter_path}"

    # Dynamically import filter.py
    spec = importlib.util.spec_from_file_location("filter_module", filter_path)
    filter_module = importlib.util.module_from_spec(spec)
    sys.modules["filter_module"] = filter_module
    try:
        spec.loader.exec_module(filter_module)
    except Exception as e:
        pytest.fail(f"Failed to import {filter_path}: {e}")

    assert hasattr(filter_module, "is_clean"), f"Module {filter_path} does not have an 'is_clean' function"
    is_clean = filter_module.is_clean

    evil_path = "/app/verifier/corpora/evil.txt"
    clean_path = "/app/verifier/corpora/clean.txt"

    assert os.path.isfile(evil_path), f"Missing evil corpus at {evil_path}"
    assert os.path.isfile(clean_path), f"Missing clean corpus at {clean_path}"

    with open(evil_path, "r", encoding="utf-8") as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    with open(clean_path, "r", encoding="utf-8") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    evil_bypassed = []
    for line in evil_lines:
        try:
            if is_clean(line) is not False:
                evil_bypassed.append(line)
        except Exception as e:
            pytest.fail(f"is_clean raised an exception on evil input: {e}")

    clean_modified = []
    for line in clean_lines:
        try:
            if is_clean(line) is not True:
                clean_modified.append(line)
        except Exception as e:
            pytest.fail(f"is_clean raised an exception on clean input: {e}")

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_lines)} evil bypassed")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_lines)} clean modified")

    if error_messages:
        pytest.fail(" | ".join(error_messages))