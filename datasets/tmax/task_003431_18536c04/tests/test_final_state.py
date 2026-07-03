# test_final_state.py

import os
import sys
import importlib.util
import pytest

def load_sanitizer():
    sanitizer_path = "/home/user/archiver/sanitizer.py"
    if not os.path.exists(sanitizer_path):
        pytest.fail(f"File not found: {sanitizer_path}")

    spec = importlib.util.spec_from_file_location("sanitizer", sanitizer_path)
    sanitizer = importlib.util.module_from_spec(spec)
    sys.modules["sanitizer"] = sanitizer
    try:
        spec.loader.exec_module(sanitizer)
    except Exception as e:
        pytest.fail(f"Failed to import sanitizer.py: {e}")
    return sanitizer

def test_sanitizer_adversarial_corpus():
    sanitizer = load_sanitizer()
    assert hasattr(sanitizer, "sanitize_chunk"), "Function 'sanitize_chunk' is missing from sanitizer.py"
    sanitize_chunk = sanitizer.sanitize_chunk

    evil_dir = "/home/user/archiver/corpus/evil/"
    clean_dir = "/home/user/archiver/corpus/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus directory"
    assert len(clean_files) > 0, "No files found in clean corpus directory"

    evil_bypassed = []
    for ef in evil_files:
        try:
            result = sanitize_chunk(ef)
            if result is not False:
                evil_bypassed.append(os.path.basename(ef))
        except Exception:
            evil_bypassed.append(os.path.basename(ef) + " (exception raised)")

    clean_modified = []
    for cf in clean_files:
        try:
            result = sanitize_chunk(cf)
            if result is not True:
                clean_modified.append(os.path.basename(cf))
        except Exception:
            clean_modified.append(os.path.basename(cf) + " (exception raised)")

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_api_redis_config():
    api_path = "/home/user/archiver/api.py"
    assert os.path.exists(api_path), f"File not found: {api_path}"
    with open(api_path, "r") as f:
        content = f.read()
        assert "redis.sock" in content, "api.py does not appear to be configured to use redis.sock"
        assert "6379" not in content, "api.py still contains the default TCP port 6379"

def test_worker_redis_config():
    worker_path = "/home/user/archiver/worker.py"
    assert os.path.exists(worker_path), f"File not found: {worker_path}"
    with open(worker_path, "r") as f:
        content = f.read()
        assert "redis.sock" in content, "worker.py does not appear to be configured to use redis.sock"
        assert "6379" not in content, "worker.py still contains the default TCP port 6379"

def test_worker_integration():
    worker_path = "/home/user/archiver/worker.py"
    assert os.path.exists(worker_path), f"File not found: {worker_path}"
    with open(worker_path, "r") as f:
        content = f.read()
        assert "sanitize_chunk" in content, "worker.py does not appear to use the sanitize_chunk function"
        assert "master_archive.bin" in content, "worker.py does not reference master_archive.bin"
        assert "rejected.log" in content, "worker.py does not reference rejected.log"