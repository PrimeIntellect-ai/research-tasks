# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_pipeline_directories_created():
    expected_dirs = [
        "/home/user/pipeline/logs/incoming",
        "/home/user/pipeline/logs/processed",
        "/home/user/pipeline/video_frames"
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Expected directory {d} was not created."

def test_video_alert_count():
    count_file = "/home/user/pipeline/video_alert_count.txt"
    assert os.path.isfile(count_file), f"Missing video alert count file: {count_file}"

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "27", f"Expected video alert count to be '27', but got '{content}'"

def test_filter_logs_adversarial_corpus():
    script_path = "/home/user/filter_logs.py"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    clean_corpus = "/app/corpus/clean"
    evil_corpus = "/app/corpus/evil"

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Run on clean corpus
        subprocess.run(["python3", script_path, clean_corpus, clean_out], check=False)

        # Run on evil corpus
        subprocess.run(["python3", script_path, evil_corpus, evil_out], check=False)

        clean_input_files = set(os.listdir(clean_corpus))
        clean_output_files = set(os.listdir(clean_out))

        evil_input_files = set(os.listdir(evil_corpus))
        evil_output_files = set(os.listdir(evil_out))

        # Check clean corpus
        missing_clean = clean_input_files - clean_output_files

        # Check evil corpus
        bypassed_evil = evil_output_files

        errors = []
        if missing_clean:
            errors.append(f"{len(missing_clean)} of {len(clean_input_files)} clean modified/rejected: {', '.join(missing_clean)}")
        if bypassed_evil:
            errors.append(f"{len(bypassed_evil)} of {len(evil_input_files)} evil bypassed: {', '.join(bypassed_evil)}")

        if errors:
            pytest.fail(" | ".join(errors))