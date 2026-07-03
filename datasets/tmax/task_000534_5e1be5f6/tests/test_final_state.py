# test_final_state.py

import os
import subprocess
import tempfile

def test_evidence_txt_generated_and_correct():
    evidence_path = "/home/user/evidence.txt"
    assert os.path.isfile(evidence_path), f"Evidence file {evidence_path} was not created."

    with open(evidence_path, "r") as f:
        content = f.read().strip()

    expected_secret = "FLAG-8293-SECURE-KEY-SSRF-LEAK"
    assert content == expected_secret, f"The content of {evidence_path} does not match the expected leaked secret. Found: {content}"

def test_evidence_enc_generated_and_correct():
    enc_path = "/home/user/evidence.enc"
    assert os.path.isfile(enc_path), f"Encrypted evidence file {enc_path} was not created."

    evidence = b"FLAG-8293-SECURE-KEY-SSRF-LEAK"
    key = b"COMPLIANCE_KEY_2024"
    expected_enc = bytes([evidence[i] ^ key[i % len(key)] for i in range(len(evidence))])

    with open(enc_path, "rb") as f:
        actual_enc = f.read()

    assert actual_enc == expected_enc, f"The content of {enc_path} does not match the expected XOR encrypted output."

def test_crypto_tool_compiled():
    tool_path = "/home/user/crypto_tool"
    assert os.path.isfile(tool_path), f"Compiled crypto tool {tool_path} does not exist."
    assert os.access(tool_path, os.X_OK), f"The file {tool_path} is not executable."

def test_auth_service_fixed_cpp_exists():
    cpp_path = "/home/user/auth_service_fixed.cpp"
    assert os.path.isfile(cpp_path), f"Patched source code {cpp_path} does not exist."

def test_auth_service_fixed_logic():
    cpp_path = "/home/user/auth_service_fixed.cpp"

    # Create a wrapper C++ file to test the handle_request function directly
    wrapper_cpp = """
#include <iostream>
#include <string>

// Include the student's fixed code
#include "/home/user/auth_service_fixed.cpp"

int main() {
    std::cout << "---TEST1---" << std::endl;
    std::cout << handle_request("file:///home/user/vault/secret.key") << std::endl;
    std::cout << "---TEST2---" << std::endl;
    std::cout << handle_request("http://internal.company.local/dashboard") << std::endl;
    std::cout << "---TEST3---" << std::endl;
    std::cout << handle_request("http://evil.com/malware") << std::endl;
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        wrapper_path = os.path.join(tmpdir, "wrapper.cpp")
        bin_path = os.path.join(tmpdir, "test_runner")

        with open(wrapper_path, "w") as f:
            f.write(wrapper_cpp)

        # Compile the wrapper
        compile_proc = subprocess.run(
            ["g++", wrapper_path, "-o", bin_path],
            capture_output=True,
            text=True
        )
        assert compile_proc.returncode == 0, f"Failed to compile {cpp_path}. Compiler error:\n{compile_proc.stderr}"

        # Run the wrapper
        run_proc = subprocess.run(
            [bin_path],
            capture_output=True,
            text=True
        )
        assert run_proc.returncode == 0, "The compiled test runner crashed during execution."

        output = run_proc.stdout

        # Parse outputs
        try:
            test1_out = output.split("---TEST1---")[1].split("---TEST2---")[0].strip()
            test2_out = output.split("---TEST2---")[1].split("---TEST3---")[0].strip()
            test3_out = output.split("---TEST3---")[1].strip()
        except IndexError:
            pytest.fail("Failed to parse the output from the test runner. Ensure handle_request returns a std::string.")

        expected_forbidden = "HTTP/1.1 403 Forbidden\r\n\r\nInvalid redirect"

        assert expected_forbidden in test1_out, f"Service did not reject file:// scheme correctly. Output was: {test1_out}"
        assert expected_forbidden in test3_out, f"Service did not reject external http:// scheme correctly. Output was: {test3_out}"
        assert expected_forbidden not in test2_out, f"Service incorrectly rejected valid internal URL. Output was: {test2_out}"
        assert "Redirecting to http://internal.company.local/dashboard" in test2_out, f"Service did not properly handle the valid internal URL. Output was: {test2_out}"