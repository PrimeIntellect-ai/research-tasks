# test_final_state.py

import os
import stat
import subprocess
from pathlib import Path

def test_calc_det_compiled():
    calc_det_path = Path("/home/user/bin/calc_det")
    assert calc_det_path.is_file(), f"Compiled executable not found at {calc_det_path}"
    assert os.access(calc_det_path, os.X_OK), f"File {calc_det_path} is not executable"

def test_filter_graph_script_exists_and_executable():
    script_path = Path("/home/user/filter_graph.sh")
    assert script_path.is_file(), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_adversarial_corpus():
    script_path = "/home/user/filter_graph.sh"

    evil_corpus_dir = Path("/app/corpus/evil")
    clean_corpus_dir = Path("/app/corpus/clean")

    evil_files = list(evil_corpus_dir.glob("*.txt"))
    clean_files = list(clean_corpus_dir.glob("*.txt"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    for evil_file in evil_files:
        result = subprocess.run([script_path, str(evil_file)], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(evil_file.name)

    clean_modified = []
    for clean_file in clean_files:
        result = subprocess.run([script_path, str(clean_file)], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(clean_file.name)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(evil_bypassed[:5])}{'...' if len(evil_bypassed) > 5 else ''}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected. Offending files: {', '.join(clean_modified[:5])}{'...' if len(clean_modified) > 5 else ''}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msg)