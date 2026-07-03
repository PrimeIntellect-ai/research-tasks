# test_final_state.py

import os
import hashlib
import pytest

def test_cert_verify_log():
    log_path = "/home/user/cert_verify.log"
    assert os.path.isfile(log_path), f"Missing file: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "/home/user/cert.pem: OK" in content, "cert_verify.log does not contain the expected verification success message."

def test_dropper_hash():
    dropper_path = "/home/user/dropper"
    hash_path = "/home/user/dropper_hash.txt"

    assert os.path.isfile(dropper_path), f"Missing file: {dropper_path}"
    assert os.path.isfile(hash_path), f"Missing file: {hash_path}"

    # Compute expected hash
    sha256 = hashlib.sha256()
    with open(dropper_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    expected_hash = sha256.hexdigest()

    with open(hash_path, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Hash in {hash_path} does not match the actual SHA-256 hash of {dropper_path}."

def test_dropper_output():
    output_path = "/home/user/dropper_output.txt"
    assert os.path.isfile(output_path), f"Missing file: {output_path}"

    with open(output_path, "r") as f:
        content = f.read()

    expected_output = "EXPLOIT_PAYLOAD_EXECUTION_SUCCESSFUL_C2_CONNECTING...\n"
    assert content == expected_output, "dropper_output.txt does not contain the exact expected output from the sandboxed execution."

def test_analyzer_cpp():
    cpp_path = "/home/user/analyzer.cpp"
    assert os.path.isfile(cpp_path), f"Missing file: {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "#include <openssl/sha.h>" in content, "analyzer.cpp is missing the required OpenSSL SHA header inclusion."
    assert "bwrap" in content, "analyzer.cpp does not contain the required bwrap invocation."
    assert "--ro-bind / /" in content, "analyzer.cpp does not contain the required bwrap arguments."
    assert "--dev /dev" in content, "analyzer.cpp does not contain the required bwrap arguments."
    assert "--unshare-all" in content, "analyzer.cpp does not contain the required bwrap arguments."