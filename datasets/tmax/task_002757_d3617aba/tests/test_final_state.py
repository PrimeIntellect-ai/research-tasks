# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_filter_edges_executable_exists():
    executable_path = "/home/user/filter_edges"
    assert os.path.isfile(executable_path), f"Missing executable: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_adversarial_corpus_clean():
    executable_path = "/home/user/filter_edges"
    clean_dir = "/app/corpora/clean/"
    clean_files = glob.glob(os.path.join(clean_dir, "*.csv"))
    assert clean_files, f"No clean corpus files found in {clean_dir}"

    modified_clean = []

    for file_path in clean_files:
        with open(file_path, "r") as f:
            expected_output = f.read().strip()

        result = subprocess.run([executable_path, file_path], capture_output=True, text=True)
        actual_output = result.stdout.strip()

        # Normalize line endings
        expected_output = "\n".join(line.strip() for line in expected_output.splitlines() if line.strip())
        actual_output = "\n".join(line.strip() for line in actual_output.splitlines() if line.strip())

        if actual_output != expected_output:
            modified_clean.append(os.path.basename(file_path))

    assert not modified_clean, f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}"

def test_adversarial_corpus_evil():
    executable_path = "/home/user/filter_edges"
    evil_dir = "/app/corpora/evil/"
    evil_files = glob.glob(os.path.join(evil_dir, "*.csv"))
    assert evil_files, f"No evil corpus files found in {evil_dir}"

    bypassed_evil = []

    for file_path in evil_files:
        with open(file_path, "r") as f:
            header = f.readline().strip()

        result = subprocess.run([executable_path, file_path], capture_output=True, text=True)
        actual_output = result.stdout.strip()

        actual_lines = [line.strip() for line in actual_output.splitlines() if line.strip()]

        # Output should only contain the header
        if len(actual_lines) != 1 or actual_lines[0] != header:
            bypassed_evil.append(os.path.basename(file_path))

    assert not bypassed_evil, f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}"

def test_final_report_content():
    report_path = "/home/user/final_report.csv"
    assert os.path.isfile(report_path), f"Missing final report: {report_path}"

    expected_lines = [
        "source_id,target_id,weight,rank",
        "2,6,200,2",
        "2,7,150,3",
        "3,5,600,1",
        "3,11,90,2",
        "4,17,20,1",
        "4,3,10,2",
        "4,10,10,3",
        "5,1,100,1",
        "5,3,20,2",
        "5,2,10,3",
        "6,1,50,1"
    ]

    with open(report_path, "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Final report content does not match expected output. Got: {actual_lines}"