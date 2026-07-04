# test_final_state.py

import os
import re
import pytest

def test_cpp_fixed():
    path = "/home/user/audit_parser.cpp"
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "r") as f:
        content = f.read()

    # Check that strcpy is no longer used for the buffer
    assert "strcpy(buffer" not in content, "Vulnerable 'strcpy(buffer' is still present in the C++ code."

def test_executable_exists():
    path = "/home/user/audit_parser"
    assert os.path.isfile(path), f"Missing executable: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_run_audit_script():
    path = "/home/user/run_audit.sh"
    assert os.path.isfile(path), f"Missing script: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "bwrap" in content, "Script does not use 'bwrap'."
    assert "--unshare-all" in content, "Script does not contain '--unshare-all' flag for bwrap."

    # Check for read-only bind of root
    assert re.search(r"--ro-bind\s+/\s+/", content), "Script does not contain '--ro-bind / /' for bwrap."

def test_output_generated():
    output_dir = "/home/user/audit_output"
    output_file = os.path.join(output_dir, "decrypted_trail.txt")

    assert os.path.isdir(output_dir), f"Missing directory: {output_dir}"
    assert os.path.isfile(output_file), f"Missing output file: {output_file}"

    with open(output_file, "r") as f:
        content = f.read()

    assert "AUDIT_RECORD:" in content, "Output file does not contain the expected decrypted audit records."
    # Ensure it's not empty and successfully parsed
    assert len(content.strip()) > 0, "Output file is empty."