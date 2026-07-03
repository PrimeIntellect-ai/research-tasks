# test_final_state.py

import os
import subprocess
import pytest

def test_tool_exists_and_executable():
    tool_path = "/home/user/dataset_tool"
    assert os.path.isfile(tool_path), f"Executable {tool_path} not found. Did you compile your program?"
    assert os.access(tool_path, os.X_OK), f"File {tool_path} is not executable."

def test_source_code_locking():
    source_path = "/home/user/dataset_tool.c"
    assert os.path.isfile(source_path), f"Source file {source_path} not found."
    with open(source_path, "r") as f:
        content = f.read()

    has_flock = "flock" in content
    has_fcntl = "fcntl" in content and ("F_SETLKW" in content or "F_SETLK" in content)
    assert has_flock or has_fcntl, "Source code does not appear to use POSIX file locking (flock or fcntl with F_SETLKW)."

def test_adversarial_corpus_verification():
    tool_path = "/home/user/dataset_tool"
    evil_corpus_dir = "/app/verifier/evil_corpus/"
    clean_corpus_dir = "/app/verifier/clean_corpus/"

    assert os.path.isdir(evil_corpus_dir), "Evil corpus directory missing."
    assert os.path.isdir(clean_corpus_dir), "Clean corpus directory missing."

    evil_files = [os.path.join(evil_corpus_dir, f) for f in os.listdir(evil_corpus_dir) if os.path.isfile(os.path.join(evil_corpus_dir, f))]
    clean_files = [os.path.join(clean_corpus_dir, f) for f in os.listdir(clean_corpus_dir) if os.path.isfile(os.path.join(clean_corpus_dir, f))]

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run([tool_path, "--verify", f], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run([tool_path, "--verify", f], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(f))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil files bypassed verification: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean files were incorrectly rejected: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_clean_combined_log_validity():
    output_log = "/home/user/dataset/clean_combined.log"
    assert os.path.isfile(output_log), f"Output file {output_log} not found. Did you run the --build command?"

    with open(output_log, "r") as f:
        lines = f.readlines()

    in_record = False
    fault_flag = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        if line == "BEGIN_RECORD":
            assert not in_record, f"Interleaved or nested BEGIN_RECORD found at line {i+1}."
            in_record = True
            fault_flag = False
        elif line == "END_RECORD":
            assert in_record, f"END_RECORD found without BEGIN_RECORD at line {i+1}."
            assert not fault_flag, f"Invalid record containing unoverridden STATUS: FAULT was written to the output log (ending at line {i+1})."
            in_record = False
        elif in_record:
            if line == "STATUS: FAULT":
                fault_flag = True
            elif line == "OVERRIDE: TRUE":
                fault_flag = False
        else:
            pytest.fail(f"Line {i+1} ('{line}') is outside of a BEGIN_RECORD/END_RECORD block, indicating interleaved or malformed writes.")

    assert not in_record, "File ended with an unclosed BEGIN_RECORD block."