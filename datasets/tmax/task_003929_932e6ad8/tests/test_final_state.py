# test_final_state.py

import os
import stat
import pytest

def test_mitigation_script():
    script_path = "/home/user/mitigation.sh"

    assert os.path.exists(script_path), f"File {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), f"File {script_path} is not executable."

    with open(script_path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "#!/bin/bash",
        "iptables -A INPUT -s 198.51.100.22 -j DROP"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Content of {script_path} does not match expected output."

def test_csp_header():
    csp_path = "/home/user/csp_header.txt"

    assert os.path.exists(csp_path), f"File {csp_path} is missing."
    assert os.path.isfile(csp_path), f"{csp_path} is not a file."

    with open(csp_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Content-Security-Policy: default-src 'none';"

    assert content == expected_content, f"Content of {csp_path} does not match expected output. Got: {content}"