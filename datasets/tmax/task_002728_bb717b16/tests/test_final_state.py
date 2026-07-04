# test_final_state.py

import os
import subprocess
import pytest

def test_secret_key_extracted():
    secret_path = "/app/jwt-service/secret.key"
    assert os.path.isfile(secret_path), f"Secret key file not found at {secret_path}"

    with open(secret_path, "r") as f:
        secret = f.read().strip()

    expected_secret = "X9fR2mP7qL4cT1vN8bH5wK3zJ6yD0sA!"
    assert secret == expected_secret, f"Secret key extracted is incorrect. Expected {expected_secret}, got {secret}"

def test_tls_certificates_exist():
    cert_path = "/app/jwt-service/tls/cert.pem"
    key_path = "/app/jwt-service/tls/key.pem"

    assert os.path.isfile(cert_path), f"TLS certificate not found at {cert_path}"
    assert os.path.isfile(key_path), f"TLS private key not found at {key_path}"

    # Check if they are non-empty
    assert os.path.getsize(cert_path) > 0, "TLS certificate is empty"
    assert os.path.getsize(key_path) > 0, "TLS private key is empty"

def test_makefile_fixed():
    makefile_path = "/app/jwt-service/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-lssl" in content, "Makefile is missing -lssl linker flag"
    assert "-lcrypto" in content, "Makefile is missing -lcrypto linker flag"

def test_auth_cpp_vulnerability_patched(tmp_path):
    # We will compile a small C++ program linking against the modified auth.cpp
    # to verify the logic.
    auth_cpp_path = "/app/jwt-service/src/auth.cpp"
    auth_h_path = "/app/jwt-service/src/auth.h"

    assert os.path.isfile(auth_cpp_path), f"auth.cpp not found at {auth_cpp_path}"

    test_cpp_content = """
#include <iostream>
#include "auth.h"

int main() {
    std::string secret = "X9fR2mP7qL4cT1vN8bH5wK3zJ6yD0sA!";

    // Test 1: alg=none bypass should fail
    if (verify_jwt("header.payload.alg=none", secret)) {
        std::cerr << "FAIL_ALG_NONE" << std::endl;
        return 1;
    }
    if (verify_jwt("header.payload.alg=NONE", secret)) {
        std::cerr << "FAIL_ALG_NONE" << std::endl;
        return 1;
    }

    // Test 2: Valid signature should pass
    if (!verify_jwt("header.payload." + secret, secret)) {
        std::cerr << "FAIL_VALID_SIG" << std::endl;
        return 1;
    }

    std::cout << "SUCCESS" << std::endl;
    return 0;
}
    """

    test_cpp_path = tmp_path / "test_auth.cpp"
    test_cpp_path.write_text(test_cpp_content)

    binary_path = tmp_path / "test_auth"

    # Compile the test program
    compile_cmd = [
        "g++", "-std=c++11", 
        str(test_cpp_path), 
        auth_cpp_path, 
        "-I/app/jwt-service/src", 
        "-o", str(binary_path)
    ]

    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Failed to compile test program against auth.cpp:\n{compile_proc.stderr}"

    # Run the test program
    run_proc = subprocess.run([str(binary_path)], capture_output=True, text=True)
    assert run_proc.returncode == 0, f"Vulnerability test failed. Output: {run_proc.stderr.strip()}"
    assert "SUCCESS" in run_proc.stdout, "Vulnerability test did not output SUCCESS"

def test_service_compiled():
    binary_path = "/app/jwt-service/jwt_server"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}. Did you run make?"
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable"