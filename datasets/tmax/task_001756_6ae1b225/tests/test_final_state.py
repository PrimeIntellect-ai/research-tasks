# test_final_state.py
import os
import subprocess
import pytest

def run_doc_filter(target_dir):
    executable = "/home/user/doc_filter"
    config_file = "/home/user/doc_rules.conf"

    assert os.path.isfile(executable), f"Executable not found at {executable}"
    assert os.access(executable, os.X_OK), f"Executable at {executable} is not executable"

    try:
        result = subprocess.run(
            [executable, config_file, target_dir],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return result.stdout.strip().splitlines()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of doc_filter failed with return code {e.returncode}. Output: {e.stdout}\nError: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail("Execution of doc_filter timed out.")

def parse_output(output_lines):
    results = {}
    for line in output_lines:
        line = line.strip()
        if not line:
            continue
        if ": " not in line:
            pytest.fail(f"Invalid output format (missing ': '): '{line}'")
        filename, status = line.split(": ", 1)
        results[filename] = status
    return results

def test_clean_corpus():
    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    expected_files = sorted([f for f in os.listdir(clean_dir) if f.endswith('.zip')])
    output_lines = run_doc_filter(clean_dir)
    results = parse_output(output_lines)

    modified_files = []
    missing_files = []

    for filename in expected_files:
        if filename not in results:
            missing_files.append(filename)
        elif results[filename] != "CLEAN":
            modified_files.append(filename)

    error_msgs = []
    if missing_files:
        error_msgs.append(f"{len(missing_files)} of {len(expected_files)} clean missing from output: {missing_files}")
    if modified_files:
        error_msgs.append(f"{len(modified_files)} of {len(expected_files)} clean modified (not CLEAN): {modified_files}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_evil_corpus():
    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    expected_files = sorted([f for f in os.listdir(evil_dir) if f.endswith('.zip')])
    output_lines = run_doc_filter(evil_dir)
    results = parse_output(output_lines)

    bypassed_files = []
    missing_files = []

    for filename in expected_files:
        if filename not in results:
            missing_files.append(filename)
        elif results[filename] != "REJECT":
            bypassed_files.append(filename)

    error_msgs = []
    if missing_files:
        error_msgs.append(f"{len(missing_files)} of {len(expected_files)} evil missing from output: {missing_files}")
    if bypassed_files:
        error_msgs.append(f"{len(bypassed_files)} of {len(expected_files)} evil bypassed (not REJECT): {bypassed_files}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))