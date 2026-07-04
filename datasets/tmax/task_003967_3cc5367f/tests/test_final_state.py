# test_final_state.py
import os
import subprocess
import pytest

def run_filter_pdb(directory):
    executable = "/home/user/filter_pdb"
    assert os.path.isfile(executable), f"Executable {executable} not found."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

    result = subprocess.run([executable, directory], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution failed for {directory} with stderr: {result.stderr}"

    output = result.stdout.strip().split('\n')
    parsed_results = {}
    for line in output:
        if not line.strip():
            continue
        parts = line.split(':')
        if len(parts) == 2:
            filename = os.path.basename(parts[0].strip())
            status = parts[1].strip()
            parsed_results[filename] = status

    return parsed_results

def test_clean_corpus():
    clean_dir = "/app/data/clean"
    assert os.path.isdir(clean_dir), f"Clean directory {clean_dir} missing."

    expected_files = {f for f in os.listdir(clean_dir) if f.endswith('.pdb')}
    parsed_results = run_filter_pdb(clean_dir)

    modified_clean = []
    for f in expected_files:
        if parsed_results.get(f) != "STABLE":
            modified_clean.append(f)

    if modified_clean:
        pytest.fail(f"{len(modified_clean)} of {len(expected_files)} clean modified (expected STABLE, got something else or missing): {', '.join(modified_clean)}")

def test_evil_corpus():
    evil_dir = "/app/data/evil"
    assert os.path.isdir(evil_dir), f"Evil directory {evil_dir} missing."

    expected_files = {f for f in os.listdir(evil_dir) if f.endswith('.pdb')}
    parsed_results = run_filter_pdb(evil_dir)

    bypassed_evil = []
    for f in expected_files:
        if parsed_results.get(f) != "UNSTABLE":
            bypassed_evil.append(f)

    if bypassed_evil:
        pytest.fail(f"{len(bypassed_evil)} of {len(expected_files)} evil bypassed (expected UNSTABLE, got something else or missing): {', '.join(bypassed_evil)}")