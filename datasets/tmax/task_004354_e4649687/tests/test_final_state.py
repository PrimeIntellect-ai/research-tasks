# test_final_state.py
import os
import subprocess
import pytest

def get_expected_token():
    enc_path = "/home/user/confidential.enc"
    assert os.path.exists(enc_path), f"Missing {enc_path}"
    with open(enc_path, "rb") as f:
        data = f.read()

    decrypted = bytearray()
    for byte in data:
        decrypted.append(byte ^ 0x5A)
    return decrypted.decode('utf-8', errors='ignore')

def test_flag_contents():
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"Missing {flag_path}"

    with open(flag_path, "r") as f:
        actual = f.read()

    expected = get_expected_token()
    assert actual == expected, f"Contents of {flag_path} do not match the expected decrypted token."

def test_fix_compilation_and_execution():
    fix_cpp = "/home/user/fix.cpp"
    assert os.path.exists(fix_cpp), f"Missing {fix_cpp}"

    fix_exe = "/home/user/fix"

    # Compile the patched code
    compile_proc = subprocess.run(
        ["g++", fix_cpp, "-o", fix_exe],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert compile_proc.returncode == 0, f"Compilation of {fix_cpp} failed:\n{compile_proc.stderr.decode('utf-8', errors='ignore')}"

    # Run the patched executable with an oversized payload
    expected_token = get_expected_token()
    payload = "A" * 32
    enc_path = "/home/user/confidential.enc"

    run_proc = subprocess.run(
        [fix_exe, payload, enc_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors='ignore'
    )

    assert run_proc.stdout.strip() != expected_token.strip(), "fix.cpp is still vulnerable to buffer overflow authentication bypass."
    assert run_proc.returncode != 0, f"Expected non-zero exit code for invalid oversized payload, got {run_proc.returncode}"