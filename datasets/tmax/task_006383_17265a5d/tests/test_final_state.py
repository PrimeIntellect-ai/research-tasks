# test_final_state.py

import os
import re

def test_config_file_fixed():
    """Verify the config file has the bug fixed."""
    config_path = '/home/user/curator_config.ini'
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, 'r') as f:
        content = f.read()

    assert '# BUG: ' not in content, "The '# BUG: ' prefix was not removed from the config file."
    assert re.search(r'^DESTINATION=/home/user/curated_repo$', content, re.MULTILINE), "The DESTINATION line is missing or incorrect."

def test_cpp_source_code_exists_and_uses_flock():
    """Verify the C++ source code exists and uses flock with LOCK_SH."""
    cpp_path = '/home/user/curator.cpp'
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert 'flock' in content, "The C++ program does not use 'flock'."
    assert 'LOCK_SH' in content, "The C++ program does not use 'LOCK_SH' for shared locking."

def test_binary_exists():
    """Verify the compiled binary exists and is executable."""
    bin_path = '/home/user/curator_bin'
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

def test_stable_files_output():
    """Verify the output file contains the correct stable artifact paths."""
    out_path = '/home/user/stable_files.out'
    assert os.path.isfile(out_path), f"Output file {out_path} is missing."

    with open(out_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        '/home/user/incoming/libA_v1.so',
        '/home/user/incoming/libC_v1.so'
    ]

    assert lines == expected_lines, f"Expected output {expected_lines}, but got {lines}."