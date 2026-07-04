# test_final_state.py

import os
import subprocess
import pytest

def test_vendored_package_fixed():
    gextract_bin = "/app/vendor/bash-graph-tools-1.0/bin/gextract"
    assert os.path.isfile(gextract_bin), f"Executable not found at {gextract_bin}. Did you fix the Makefile and run make install?"
    assert os.access(gextract_bin, os.X_OK), f"File at {gextract_bin} is not executable."

    result = subprocess.run([gextract_bin, "--version"], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {gextract_bin} --version failed with exit code {result.returncode}."
    assert "bash-graph-tools v1.0" in result.stdout, f"Expected output 'bash-graph-tools v1.0', got: {result.stdout}"

def test_backup_classifier_script():
    script_path = "/home/user/validate_backup.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable."

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_shards = [os.path.join(clean_dir, d) for d in os.listdir(clean_dir) if os.path.isdir(os.path.join(clean_dir, d))]
    evil_shards = [os.path.join(evil_dir, d) for d in os.listdir(evil_dir) if os.path.isdir(os.path.join(evil_dir, d))]

    clean_failed = []
    for shard in clean_shards:
        edges = os.path.join(shard, "edges.json")
        nodes = os.path.join(shard, "nodes.csv")
        if not os.path.isfile(edges) or not os.path.isfile(nodes):
            continue

        result = subprocess.run([script_path, edges, nodes], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(shard))

    evil_bypassed = []
    for shard in evil_shards:
        edges = os.path.join(shard, "edges.json")
        nodes = os.path.join(shard, "nodes.csv")
        if not os.path.isfile(edges) or not os.path.isfile(nodes):
            continue

        result = subprocess.run([script_path, edges, nodes], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(shard))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_shards)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_shards)} clean modified (rejected): {', '.join(clean_failed)}")

    if error_messages:
        pytest.fail(" | ".join(error_messages))