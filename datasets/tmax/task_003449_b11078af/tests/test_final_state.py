# test_final_state.py

import os
import pytest

def test_admin_ips_output():
    output_file = "/home/user/admin_ips.txt"
    assert os.path.isfile(output_file), f"Expected output file {output_file} does not exist."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_ips = ["192.168.1.15", "172.16.4.102"]

    assert lines == expected_ips, f"Contents of {output_file} are incorrect. Expected {expected_ips}, but got {lines}."

def test_vuln_file_output():
    vuln_file = "/home/user/vuln_file.txt"
    assert os.path.isfile(vuln_file), f"Expected output file {vuln_file} does not exist."

    with open(vuln_file, "r") as f:
        content = f.read().strip()

    expected_path = "/home/user/audit/sys_files/usr/local/bin/helper_script.sh"

    assert content == expected_path, f"Contents of {vuln_file} are incorrect. Expected '{expected_path}', but got '{content}'."

def test_cookie_extractor_cpp_exists():
    cpp_file = "/home/user/cookie_extractor.cpp"
    assert os.path.isfile(cpp_file), f"Expected C++ source file {cpp_file} does not exist."

    with open(cpp_file, "r") as f:
        content = f.read()

    assert len(content.strip()) > 0, f"File {cpp_file} exists but is empty."
    # Basic check to see if it looks like C++ code
    assert "#include" in content or "int main" in content, f"File {cpp_file} does not appear to contain valid C++ code."