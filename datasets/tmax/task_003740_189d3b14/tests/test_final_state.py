# test_final_state.py

import os
import csv
import subprocess
import tempfile
import pytest

def test_video_graph_csv():
    """Verify that the video graph was extracted correctly."""
    csv_path = '/home/user/video_graph.csv'
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['frame', 'source', 'target'], f"Incorrect header in {csv_path}: {header}"

        rows = list(reader)
        assert len(rows) == 85, f"Expected exactly 85 edges extracted from the video, but found {len(rows)}."

def test_filter_datasets_script_exists():
    """Verify that the filtering script exists."""
    script_path = '/home/user/filter_datasets.py'
    assert os.path.exists(script_path), f"Filtering script {script_path} does not exist."

def test_filter_datasets_adversarial_corpus():
    """Verify that the filtering script accepts clean files and rejects evil files."""
    script_path = '/home/user/filter_datasets.py'
    clean_in = '/app/corpus/clean'
    evil_in = '/app/corpus/evil'

    assert os.path.exists(clean_in), f"Clean corpus missing at {clean_in}"
    assert os.path.exists(evil_in), f"Evil corpus missing at {evil_in}"

    with tempfile.TemporaryDirectory() as clean_out, tempfile.TemporaryDirectory() as evil_out:
        # Run the agent's script on both corpora
        try:
            subprocess.run(['python3', script_path, clean_in, clean_out], check=True, capture_output=True, text=True)
            subprocess.run(['python3', script_path, evil_in, evil_out], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Script execution failed.\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")

        # Validate Clean Corpus
        clean_in_files = set(f for f in os.listdir(clean_in) if f.endswith('.csv'))
        clean_out_files = set(os.listdir(clean_out))

        missing_clean = clean_in_files - clean_out_files
        modified_clean = []

        for f in clean_in_files.intersection(clean_out_files):
            with open(os.path.join(clean_in, f), 'r', encoding='utf-8') as f1, open(os.path.join(clean_out, f), 'r', encoding='utf-8') as f2:
                if f1.read() != f2.read():
                    modified_clean.append(f)

        total_clean_issues = len(missing_clean) + len(modified_clean)
        if total_clean_issues > 0:
            msg = f"{total_clean_issues} of {len(clean_in_files)} clean modified or missing. "
            if missing_clean:
                msg += f"Missing: {sorted(list(missing_clean))}. "
            if modified_clean:
                msg += f"Modified: {sorted(modified_clean)}."
            pytest.fail(msg)

        # Validate Evil Corpus
        evil_in_files = set(f for f in os.listdir(evil_in) if f.endswith('.csv'))
        evil_out_files = set(os.listdir(evil_out))

        bypassed_evil = evil_out_files.intersection(evil_in_files)
        if bypassed_evil:
            pytest.fail(f"{len(bypassed_evil)} of {len(evil_in_files)} evil bypassed. Offending files: {sorted(list(bypassed_evil))}")