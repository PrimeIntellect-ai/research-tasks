# test_final_state.py

import os
import subprocess
import glob
import pytest

def test_compiled_profiler_exists():
    profiler_path = "/home/user/seq_profiler"
    assert os.path.isfile(profiler_path), f"Compiled profiler not found at {profiler_path}."
    assert os.access(profiler_path, os.X_OK), f"Compiled profiler at {profiler_path} is not executable."

def test_filter_script_exists():
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Filter script not found at {script_path}."
    assert os.access(script_path, os.X_OK) or os.access(script_path, os.R_OK), f"Filter script at {script_path} is not readable/executable."

def test_clean_corpus_accepted():
    script_path = "/home/user/filter.sh"
    clean_dir = "/app/corpus/clean"
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."

    failed_files = []
    for filepath in clean_files:
        result = subprocess.run(["bash", script_path, filepath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files were incorrectly rejected (modified/failed): {', '.join(failed_files)}")

def test_evil_corpus_rejected():
    script_path = "/home/user/filter.sh"
    evil_dir = "/app/corpus/evil"
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."

    failed_files = []
    for filepath in evil_files:
        result = subprocess.run(["bash", script_path, filepath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(filepath))

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed the filter (accepted when they should be rejected): {', '.join(failed_files)}")