# test_final_state.py

import os
import re
import subprocess
import pytest

def test_pipeline_configs():
    """Verify that the pipeline configuration files have the correct ports set."""
    streamer_env_path = '/app/pipeline/config/streamer.env'
    analyzer_toml_path = '/app/pipeline/config/analyzer.toml'
    sink_env_path = '/app/pipeline/config/sink.env'

    assert os.path.isfile(streamer_env_path), f"{streamer_env_path} is missing"
    with open(streamer_env_path, 'r') as f:
        streamer_env = f.read()
    assert re.search(r'^TARGET_PORT\s*=\s*"?5001"?', streamer_env, re.MULTILINE), \
        "streamer.env TARGET_PORT is not correctly set to 5001"

    assert os.path.isfile(analyzer_toml_path), f"{analyzer_toml_path} is missing"
    with open(analyzer_toml_path, 'r') as f:
        analyzer_toml = f.read()
    assert re.search(r'^listen_port\s*=\s*5001', analyzer_toml, re.MULTILINE), \
        "analyzer.toml listen_port is not correctly set to 5001"
    assert re.search(r'^sink_port\s*=\s*5002', analyzer_toml, re.MULTILINE), \
        "analyzer.toml sink_port is not correctly set to 5002"

    assert os.path.isfile(sink_env_path), f"{sink_env_path} is missing"
    with open(sink_env_path, 'r') as f:
        sink_env = f.read()
    assert re.search(r'^LISTEN_PORT\s*=\s*"?5002"?', sink_env, re.MULTILINE), \
        "sink.env LISTEN_PORT is not correctly set to 5002"

def test_adversarial_corpus():
    """Verify that the filter_cli correctly accepts clean files and rejects evil files."""
    cli_path = "/app/math-analyzer/target/debug/filter_cli"
    assert os.path.isfile(cli_path), f"CLI binary not found at {cli_path}. Did you compile it?"
    assert os.access(cli_path, os.X_OK), f"CLI binary {cli_path} is not executable."

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    assert os.path.isdir(clean_dir), f"{clean_dir} directory is missing"
    assert os.path.isdir(evil_dir), f"{evil_dir} directory is missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "Clean corpus is empty"
    assert len(evil_files) > 0, "Evil corpus is empty"

    clean_failed = []
    for fpath in clean_files:
        try:
            res = subprocess.run([cli_path, fpath], capture_output=True, text=True, timeout=5)
            if res.returncode != 0 or res.stdout.strip() != "ACCEPT":
                clean_failed.append(os.path.basename(fpath))
        except subprocess.TimeoutExpired:
            clean_failed.append(os.path.basename(fpath) + " (timeout)")
        except Exception as e:
            clean_failed.append(os.path.basename(fpath) + f" (error: {e})")

    evil_failed = []
    for fpath in evil_files:
        try:
            res = subprocess.run([cli_path, fpath], capture_output=True, text=True, timeout=5)
            if res.returncode != 1 or res.stdout.strip() != "REJECT":
                evil_failed.append(os.path.basename(fpath))
        except subprocess.TimeoutExpired:
            evil_failed.append(os.path.basename(fpath) + " (timeout)")
        except Exception as e:
            evil_failed.append(os.path.basename(fpath) + f" (error: {e})")

    err_msg = []
    if clean_failed:
        err_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:10])}")
    if evil_failed:
        err_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed[:10])}")

    assert not err_msg, " | ".join(err_msg)