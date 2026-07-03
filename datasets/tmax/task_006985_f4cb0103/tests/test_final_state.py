# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_attacker_ip_file():
    """Test that the attacker IP was correctly identified and written to the file."""
    filepath = "/home/user/attacker_ip.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing"

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "10.13.37.100", f"Incorrect IP address found in {filepath}. Expected '10.13.37.100', got '{content}'"

def test_auth_checker_code_fixed():
    """Test that the strcpy vulnerability was removed from auth_checker.c."""
    filepath = "/home/user/evidence/auth_checker.c"
    assert os.path.isfile(filepath), f"File {filepath} is missing"

    with open(filepath, "r") as f:
        content = f.read()

    # The exact vulnerable line should be removed or changed
    # We check that strcpy is not used blindly on user_buf and username
    # This is a basic check; the compilation and execution test is more robust.
    assert "strcpy(user_buf, username);" not in content, "The vulnerable strcpy(user_buf, username); is still present in the code."

def test_auth_checker_compilation_and_execution():
    """Test that auth_checker.c compiles and prevents the buffer overflow exploit."""
    source_file = "/home/user/evidence/auth_checker.c"
    assert os.path.isfile(source_file), f"File {source_file} is missing"

    with tempfile.TemporaryDirectory() as tmpdir:
        binary_path = os.path.join(tmpdir, "auth_checker")

        # Compile the modified C file
        compile_process = subprocess.run(
            ["gcc", "-Wall", "-Werror", source_file, "-o", binary_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert compile_process.returncode == 0, f"Compilation failed or had warnings:\n{compile_process.stderr}"

        # Test valid admin login
        admin_process = subprocess.run(
            [binary_path, "admin", "supersecret"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert admin_process.returncode == 0, "Valid admin login failed."
        assert "Admin access granted." in admin_process.stdout, "Valid admin login output is incorrect."

        # Test invalid normal login
        invalid_process = subprocess.run(
            [binary_path, "guest", "password"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert invalid_process.returncode == 1, "Invalid login should return 1."
        assert "Access denied." in invalid_process.stdout, "Invalid login output is incorrect."

        # Test exploit payload
        exploit_process = subprocess.run(
            [binary_path, "AAAAAAAAAAAAAAAAB", "dummy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        assert exploit_process.returncode == 1, "Exploit payload bypassed authentication (returned 0)."
        assert "Access denied." in exploit_process.stdout, "Exploit payload did not result in 'Access denied.'"