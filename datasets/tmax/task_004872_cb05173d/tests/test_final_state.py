# test_final_state.py

import os
import re
import subprocess
import pytest

def test_cwe_file():
    cwe_path = "/home/user/cwe.txt"
    assert os.path.isfile(cwe_path), f"File {cwe_path} is missing."
    with open(cwe_path, "r") as f:
        content = f.read().strip()
    assert "CWE-295" in content, f"Expected 'CWE-295' in {cwe_path}, but got '{content}'."

def test_redacted_output():
    output_path = "/home/user/redacted_output.log"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    expected_output = """[INFO] Transaction 101 started. User: alice.
[DEBUG] Processing payment method: XXXX-XXXX-XXXX-XXXX
[INFO] Transaction 101 successful.
[DEBUG] User bob backup payment: XXXX-XXXX-XXXX-XXXX (Visa)
[INFO] End of log."""

    with open(output_path, "r") as f:
        content = f.read().strip()

    assert content == expected_output, "The content of redacted_output.log does not match the expected redacted log."

def test_fixed_checker_content():
    go_path = "/home/user/fixed_checker.go"
    assert os.path.isfile(go_path), f"File {go_path} is missing."

    with open(go_path, "r") as f:
        content = f.read()

    assert "x509.NewCertPool(" in content or "x509.NewCertPool ()" in content, "fixed_checker.go does not use x509.NewCertPool()."
    assert "x509.VerifyOptions" in content, "fixed_checker.go does not use x509.VerifyOptions."

    has_regex_1 = re.search(r'\[0-9\]\{4\}-\[0-9\]\{4\}-\[0-9\]\{4\}-\[0-9\]\{4\}', content)
    has_regex_2 = re.search(r'\\d\{4\}-\\d\{4\}-\\d\{4\}-\\d\{4\}', content)
    assert has_regex_1 or has_regex_2, "fixed_checker.go does not contain the expected regex for credit card redaction."

def test_fixed_checker_compiles():
    go_path = "/home/user/fixed_checker.go"
    assert os.path.isfile(go_path), f"File {go_path} is missing."

    result = subprocess.run(["go", "build", "-o", "/dev/null", go_path], capture_output=True, text=True)
    assert result.returncode == 0, f"fixed_checker.go failed to compile:\n{result.stderr}"