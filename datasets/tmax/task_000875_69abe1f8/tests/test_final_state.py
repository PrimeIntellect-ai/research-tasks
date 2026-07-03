# test_final_state.py

import os
import subprocess
import pytest

def test_rust_project_compiles():
    """Check if the Rust project compiles successfully."""
    project_dir = "/home/user/rust_server"
    assert os.path.isdir(project_dir), f"Rust project directory missing at {project_dir}"

    result = subprocess.run(
        ["cargo", "build"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result.returncode == 0, f"Rust project failed to compile:\n{result.stderr.decode('utf-8')}"

def test_python_filter_corpus():
    """Check the Python filter against the adversarial corpus."""
    filter_script = "/home/user/filter.py"
    assert os.path.isfile(filter_script), f"Filter script missing at {filter_script}"

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    evil_files = sorted([f for f in os.listdir(evil_dir) if f.endswith(".json")])
    clean_files = sorted([f for f in os.listdir(clean_dir) if f.endswith(".json")])

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        path = os.path.join(evil_dir, f)
        with open(path, "r") as file:
            content = file.read()

        result = subprocess.run(
            ["python3", filter_script, content],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode == 0:
            evil_bypassed.append(f)

    for f in clean_files:
        path = os.path.join(clean_dir, f)
        with open(path, "r") as file:
            content = file.read()

        result = subprocess.run(
            ["python3", filter_script, content],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if result.returncode != 0:
            clean_modified.append(f)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_messages, " | ".join(error_messages)