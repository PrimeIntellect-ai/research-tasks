# test_final_state.py

import os
import sys
import time
import subprocess
import importlib.util
import pytest

def test_redis_port_configured():
    env_path = "/app/services/emitter/.env"
    assert os.path.isfile(env_path), f"Configuration file {env_path} is missing."
    with open(env_path, "r") as f:
        content = f.read()
    assert "REDIS_PORT=6379" in content, "REDIS_PORT was not corrected to 6379 in the .env file."

def test_worker_script_modified():
    worker_path = "/app/services/worker/worker.py"
    assert os.path.isfile(worker_path), f"Worker script {worker_path} is missing."
    with open(worker_path, "r") as f:
        content = f.read()
    assert "filter_corpus" in content, "The worker script does not import 'filter_corpus'."
    assert "check_matrix" in content, "The worker script does not use the 'check_matrix' function."

def test_adversarial_corpus_filter():
    filter_path = "/home/user/filter_corpus.py"
    assert os.path.isfile(filter_path), f"Filter script {filter_path} is missing."

    # Load the module
    spec = importlib.util.spec_from_file_location("filter_corpus", filter_path)
    filter_corpus = importlib.util.module_from_spec(spec)
    sys.modules["filter_corpus"] = filter_corpus
    spec.loader.exec_module(filter_corpus)

    assert hasattr(filter_corpus, "check_matrix"), "Function 'check_matrix' is missing in filter_corpus.py."
    check_matrix = filter_corpus.check_matrix

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]

    clean_modified = []
    evil_bypassed = []

    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        if not check_matrix(filepath):
            clean_modified.append(f)

    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        if check_matrix(filepath):
            evil_bypassed.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not errors, "Adversarial corpus verification failed: " + "; ".join(errors)

def test_end_to_end_flow():
    start_script = "/app/services/start.sh"
    assert os.path.isfile(start_script), f"Start script {start_script} is missing."

    # Clean up previous log if any
    log_path = "/app/services/worker/success.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    # Launch the services
    process = subprocess.Popen([start_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)

    try:
        # Wait 10 seconds for the pipeline to process data
        time.sleep(10)

        # Check if process is still running (or its children)
        # We just check if the success log has been created and has entries
        assert os.path.isfile(log_path), f"Success log {log_path} was not created. The worker might have crashed or failed."

        with open(log_path, "r") as f:
            lines = [line for line in f.read().splitlines() if line.strip()]

        assert len(lines) >= 3, f"Expected at least 3 entries in {log_path}, but found {len(lines)}."
    finally:
        # Cleanup process
        import signal
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception:
            pass