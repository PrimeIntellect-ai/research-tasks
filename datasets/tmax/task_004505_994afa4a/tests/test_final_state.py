# test_final_state.py

import os
import subprocess
import pytest

def test_part1_malicious_session_extracted():
    output_file = "/home/user/malicious_session.txt"
    assert os.path.exists(output_file), f"Output file missing: {output_file}"

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_session_id = "77B-XYZ-912"
    assert content == expected_session_id, f"Extracted session ID is incorrect. Expected '{expected_session_id}', got '{content}'"

def test_part2_query_auditor_script_exists_and_executable():
    script_path = "/home/user/query_auditor.sh"
    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_part2_query_auditor_clean_corpus():
    script_path = "/home/user/query_auditor.sh"
    clean_dir = "/app/corpus/clean"

    assert os.path.exists(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith(".json")]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_clean = []
    for cf in clean_files:
        result = subprocess.run([script_path, cf], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean files rejected (should be accepted/exit 0): {', '.join(failed_clean)}")

def test_part2_query_auditor_evil_corpus():
    script_path = "/home/user/query_auditor.sh"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith(".json")]
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_evil = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    if failed_evil:
        pytest.fail(f"{len(failed_evil)} of {len(evil_files)} evil files bypassed (should be rejected/exit 1): {', '.join(failed_evil)}")