# test_final_state.py

import os
import gzip
import stat
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/pack_docs.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_archive_exists():
    archive_path = "/home/user/archive/docs_custom.gz"
    assert os.path.isfile(archive_path), f"The archive {archive_path} does not exist."

def test_archive_contents():
    archive_path = "/home/user/archive/docs_custom.gz"
    assert os.path.isfile(archive_path), f"The archive {archive_path} does not exist."

    expected_content = """===FILE: endpoints.md===
# API Endpoints
These are the endpoints.
Copyright 2024 Acme Global
===FILE: setup.txt===
Setup Guide
Please follow these steps.
Copyright 2024 Acme Global
===FILE: readme.md===
# Main Readme
Welcome to the docs.
Copyright 2024 Acme Global. All rights reserved.
"""

    with gzip.open(archive_path, 'rt', encoding='utf-8') as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The decompressed content of the archive does not match the expected output."