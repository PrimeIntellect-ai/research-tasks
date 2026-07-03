# test_final_state.py

import os
import subprocess
import pytest

def test_vendored_package_fixed():
    process_entry_path = "/app/vendored/bash-log-utils-1.4.0/process_entry.sh"
    assert os.path.isfile(process_entry_path), f"Missing vendored process_entry.sh at {process_entry_path}"

    # Check that it runs successfully on a standard log entry without infinite recursion
    try:
        result = subprocess.run(
            [process_entry_path, "standard log entry"],
            capture_output=True,
            text=True,
            timeout=5  # Should terminate quickly if infinite recursion is fixed
        )
        assert result.returncode == 0, f"process_entry.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        pytest.fail("process_entry.sh timed out, likely due to infinite recursion not being fixed.")

def test_recovered_logs():
    recovered_log_path = "/home/user/crash_evidence.log"
    assert os.path.isfile(recovered_log_path), f"Missing recovered log at {recovered_log_path}"

    inode_table_path = "/tmp/fs_recovery_img/inode_table.txt"
    blocks_dir = "/tmp/fs_recovery_img/blocks"

    # Reconstruct expected content
    expected_content = []
    with open(inode_table_path, 'r') as f:
        for line in f:
            block_name = line.strip()
            if block_name:
                block_path = os.path.join(blocks_dir, block_name)
                if os.path.isfile(block_path):
                    with open(block_path, 'r') as bf:
                        expected_content.append(bf.read())

    expected_text = "".join(expected_content)

    with open(recovered_log_path, 'r') as f:
        actual_text = f.read()

    assert actual_text == expected_text, "Recovered crash_evidence.log content does not match the reconstructed blocks."

def test_sanitizer_filter():
    sanitize_script = "/home/user/sanitize.sh"
    assert os.path.isfile(sanitize_script), f"Missing sanitize.sh at {sanitize_script}"
    assert os.access(sanitize_script, os.X_OK), "sanitize.sh is not executable"

    clean_corpus_dir = "/app/corpora/clean"
    evil_corpus_dir = "/app/corpora/evil"

    clean_files = [f for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]
    evil_files = [f for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]

    clean_modified = []
    evil_bypassed = []

    # Test Clean Corpus (should be preserved exactly)
    for cf in clean_files:
        filepath = os.path.join(clean_corpus_dir, cf)
        with open(filepath, 'r') as f:
            original_content = f.read()

        try:
            result = subprocess.run(
                [sanitize_script],
                input=original_content,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0 or result.stdout != original_content:
                clean_modified.append(cf)
        except subprocess.TimeoutExpired:
            clean_modified.append(cf)

    # Test Evil Corpus (should be rejected/omitted)
    for ef in evil_files:
        filepath = os.path.join(evil_corpus_dir, ef)
        with open(filepath, 'r') as f:
            evil_content = f.read()

        try:
            result = subprocess.run(
                [sanitize_script],
                input=evil_content,
                capture_output=True,
                text=True,
                timeout=5
            )
            # Evil logs should be omitted from stdout
            if result.stdout.strip() != "":
                evil_bypassed.append(ef)
        except subprocess.TimeoutExpired:
            # If it times out, it's not correctly handling it, consider it bypassed or failed
            evil_bypassed.append(ef)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:5])}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:5])}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))