# test_final_state.py

import os
import subprocess
import time
import tempfile
import filecmp
import pytest

def test_cjson_built():
    assert os.path.exists("/app/cJSON/libcjson.a"), "/app/cJSON/libcjson.a is missing. The Makefile was not fixed or built."
    assert os.path.exists("/app/cJSON/libcjson.so"), "/app/cJSON/libcjson.so is missing. The Makefile was not fixed or built."

def test_sanitizer_executable():
    sanitizer = "/home/user/log_sanitizer"
    assert os.path.exists(sanitizer), f"{sanitizer} is missing."
    assert os.access(sanitizer, os.X_OK), f"{sanitizer} is not executable."

def test_adversarial_corpus():
    sanitizer = "/home/user/log_sanitizer"
    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    with tempfile.TemporaryDirectory() as tmpdir:
        for f in evil_files:
            in_path = os.path.join(evil_dir, f)
            out_path = os.path.join(tmpdir, f + ".out")
            subprocess.run([sanitizer, in_path, out_path], check=True)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                evil_bypassed.append(f)

        for f in clean_files:
            in_path = os.path.join(clean_dir, f)
            out_path = os.path.join(tmpdir, f + ".out")
            subprocess.run([sanitizer, in_path, out_path], check=True)
            if not os.path.exists(out_path) or not filecmp.cmp(in_path, out_path, shallow=False):
                clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_atomic_write_implemented():
    src_file = "/home/user/log_sanitizer.c"
    assert os.path.exists(src_file), f"{src_file} is missing."
    with open(src_file, "r") as f:
        src = f.read()
    assert ".tmp" in src, "The C source does not seem to use a .tmp file for atomic writes."
    assert "rename" in src, "The C source does not seem to use rename() for atomic writes."

def test_watch_logs_script():
    script_path = "/home/user/watch_logs.sh"
    assert os.path.exists(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    test_file = "test_integration.log"
    in_path = os.path.join("/var/spool/incoming_logs", test_file)
    out_path = os.path.join("/var/log/sanitized_logs", test_file)

    if os.path.exists(out_path):
        os.remove(out_path)

    # Write test file to trigger inotifywait
    with open(in_path, "w") as f:
        f.write('{"message": "hello"}\n')
        f.write('{"core_dump": "bad"}\n')

    # Give the background script time to process
    time.sleep(2)

    assert os.path.exists(out_path), f"Integration test failed: {out_path} was not created. Is watch_logs.sh running in the background?"
    with open(out_path, "r") as f:
        content = f.read()
    assert '{"message": "hello"}\n' in content, "Clean log not preserved in integration test."
    assert "core_dump" not in content, "Evil log not filtered in integration test."