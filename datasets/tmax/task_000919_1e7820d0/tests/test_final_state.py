# test_final_state.py

import os
import shutil
import subprocess
import tempfile
import pytest

def test_pipeline_status_log():
    log_path = "/home/user/pipeline_status.log"
    assert os.path.exists(log_path), f"Missing pipeline status log: {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
    assert "PIPELINE_SUCCESS" in content, "Pipeline status log does not contain 'PIPELINE_SUCCESS'"

def test_filter_trajectories_executable():
    executable_path = "/home/user/bin/filter_trajectories"
    assert os.path.exists(executable_path), f"Missing executable: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_adversarial_corpus():
    executable_path = "/home/user/bin/filter_trajectories"
    evil_corpus_dir = "/app/data/corpus/evil"
    clean_corpus_dir = "/app/data/corpus/clean"

    assert os.path.isdir(evil_corpus_dir), f"Missing evil corpus: {evil_corpus_dir}"
    assert os.path.isdir(clean_corpus_dir), f"Missing clean corpus: {clean_corpus_dir}"

    evil_files = set(os.listdir(evil_corpus_dir))
    clean_files = set(os.listdir(clean_corpus_dir))

    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy all corpus files to the temp directory
        for f in evil_files:
            shutil.copy(os.path.join(evil_corpus_dir, f), os.path.join(temp_dir, f))
        for f in clean_files:
            shutil.copy(os.path.join(clean_corpus_dir, f), os.path.join(temp_dir, f))

        # Run the student's filter_trajectories script on the temp directory
        try:
            result = subprocess.run(
                [executable_path, temp_dir],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0, f"filter_trajectories failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
        except subprocess.TimeoutExpired:
            pytest.fail("filter_trajectories timed out after 30 seconds")

        # Check the resulting files
        remaining_files = set(os.listdir(temp_dir))

        evil_bypassed = evil_files.intersection(remaining_files)
        clean_deleted = clean_files.difference(remaining_files)

        error_messages = []
        if evil_bypassed:
            error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(list(evil_bypassed)[:5])}")
        if clean_deleted:
            error_messages.append(f"{len(clean_deleted)} of {len(clean_files)} clean modified/deleted: {', '.join(list(clean_deleted)[:5])}")

        if error_messages:
            pytest.fail(" | ".join(error_messages))