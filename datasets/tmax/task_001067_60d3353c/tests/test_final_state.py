# test_final_state.py

import os
import stat
import pytest

def test_process_script_exists_and_configured():
    script_path = "/home/user/process.sh"
    assert os.path.exists(script_path), f"Failed: {script_path} does not exist."
    assert os.path.isfile(script_path), f"Failed: {script_path} is not a file."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Failed: {script_path} is not executable."

    # Check for OMP_NUM_THREADS
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "export OMP_NUM_THREADS=1" in content, f"Failed: 'export OMP_NUM_THREADS=1' not found in {script_path}."

def test_tokenized_txt():
    tokenized_path = "/home/user/tokenized.txt"
    assert os.path.exists(tokenized_path), f"Failed: {tokenized_path} does not exist."

    with open(tokenized_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 44, f"Failed: {tokenized_path} should contain exactly 44 words, but has {len(lines)}."
    for word in lines:
        assert word.isalpha() and word.islower(), f"Failed: Word '{word}' in {tokenized_path} is not strictly lowercase alphabetic."

def test_fold_sizes():
    f1_path = "/home/user/fold_1.txt"
    f2_path = "/home/user/fold_2.txt"
    f3_path = "/home/user/fold_3.txt"

    assert os.path.exists(f1_path), f"Failed: {f1_path} does not exist."
    assert os.path.exists(f2_path), f"Failed: {f2_path} does not exist."
    assert os.path.exists(f3_path), f"Failed: {f3_path} does not exist."

    with open(f1_path, 'r', encoding='utf-8') as f:
        f1_lines = len([line for line in f if line.strip()])
    with open(f2_path, 'r', encoding='utf-8') as f:
        f2_lines = len([line for line in f if line.strip()])
    with open(f3_path, 'r', encoding='utf-8') as f:
        f3_lines = len([line for line in f if line.strip()])

    assert f1_lines == 15, f"Failed: {f1_path} should have 15 lines, got {f1_lines}."
    assert f2_lines == 15, f"Failed: {f2_path} should have 15 lines, got {f2_lines}."
    assert f3_lines == 14, f"Failed: {f3_path} should have 14 lines, got {f3_lines}."

def test_best_param():
    param_path = "/home/user/best_param.txt"
    assert os.path.exists(param_path), f"Failed: {param_path} does not exist."

    with open(param_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content == "2", f"Failed: {param_path} should contain exactly '2', but got '{content}'."