# test_final_state.py
import os
import subprocess

def test_missing_edges_file():
    filepath = "/home/user/system_builder/missing_edges.txt"
    assert os.path.isfile(filepath), f"{filepath} is missing"

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_edges = ["core->network", "network->database", "database->render"]
    assert lines == expected_edges, f"Expected edges {expected_edges}, but got {lines}"

def test_dep_resolver_executable():
    executable = "/home/user/system_builder/dep_resolver"
    assert os.path.isfile(executable), f"Executable {executable} is missing"
    assert os.access(executable, os.X_OK), f"{executable} is not executable"

def test_adversarial_corpus():
    executable = "/home/user/system_builder/dep_resolver"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), f"{clean_dir} is missing"
    assert os.path.isdir(evil_dir), f"{evil_dir} is missing"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir)]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir)]

    failed_clean = []
    for f in clean_files:
        res = subprocess.run([executable, f], cwd="/home/user/system_builder", capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(f))

    failed_evil = []
    for f in evil_files:
        res = subprocess.run([executable, f], cwd="/home/user/system_builder", capture_output=True)
        if res.returncode == 0:
            failed_evil.append(os.path.basename(f))

    error_msg = []
    if failed_clean:
        error_msg.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected (should be accepted with exit code 0): {failed_clean[:5]}")
    if failed_evil:
        error_msg.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed (should be rejected with non-zero exit code): {failed_evil[:5]}")

    assert not failed_clean and not failed_evil, " | ".join(error_msg)