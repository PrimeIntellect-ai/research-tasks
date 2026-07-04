# test_final_state.py

import os
import pytest

def test_source_and_executable_exist():
    source_path = '/home/user/dataset_processor.c'
    executable_path = '/home/user/dataset_processor'

    assert os.path.isfile(source_path), f"Source file {source_path} is missing."
    assert os.path.isfile(executable_path), f"Executable file {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_summary_log_content():
    log_path = '/home/user/summary.log'
    assert os.path.isfile(log_path), f"Summary log {log_path} is missing."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "VALID: alpha.gz",
        "INVALID: beta.gz",
        "INVALID: gamma.gz",
        "VALID: delta.gz"
    }

    assert set(lines) == expected_lines, f"Content of {log_path} does not match expected lines."

def test_processed_files():
    processed_dir = '/home/user/processed'
    assert os.path.isdir(processed_dir), f"Directory {processed_dir} is missing."

    alpha_txt = os.path.join(processed_dir, 'alpha.txt')
    delta_txt = os.path.join(processed_dir, 'delta.txt')
    beta_txt = os.path.join(processed_dir, 'beta.txt')
    gamma_txt = os.path.join(processed_dir, 'gamma.txt')

    assert os.path.isfile(alpha_txt), f"Expected processed file {alpha_txt} is missing."
    assert os.path.isfile(delta_txt), f"Expected processed file {delta_txt} is missing."

    assert not os.path.exists(beta_txt), f"Invalid file {beta_txt} should not have been written."
    assert not os.path.exists(gamma_txt), f"Invalid file {gamma_txt} should not have been written."

    with open(alpha_txt, 'r') as f:
        alpha_content = f.read()
        assert alpha_content.count('\n') == 5, f"{alpha_txt} does not contain exactly 5 newline characters."

    with open(delta_txt, 'r') as f:
        delta_content = f.read()
        assert delta_content.count('\n') == 20, f"{delta_txt} does not contain exactly 20 newline characters."