# test_final_state.py

import os
import subprocess
import pytest

def test_ssh_keys_remediated():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"{auth_keys_path} is missing."

    with open(auth_keys_path, "r") as f:
        content = f.read()

    assert "legitimate@corp.com" in content, "Legitimate admin key was removed."
    assert "hacker@pwned" not in content, "Attacker's SSH key is still present."

def test_exploit_go_output():
    exploit_path = "/home/user/exploit.go"
    assert os.path.isfile(exploit_path), f"{exploit_path} is missing."

    result = subprocess.run(
        ["go", "run", exploit_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"exploit.go failed to run:\n{result.stderr}"

    output = result.stdout.strip()
    expected_jwt = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJyb2xlIjoiYWRtaW4ifQ."

    assert output == expected_jwt, f"exploit.go printed '{output}', expected '{expected_jwt}'"

def test_server_go_patched():
    server_path = "/home/user/app/server.go"
    assert os.path.isfile(server_path), f"{server_path} is missing."

    test_file_path = "/home/user/app/test_patch.go"
    test_code = """package main

import (
	"fmt"
	"os"
)

func main() {
	token := "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJyb2xlIjoiYWRtaW4ifQ."
	_, err := VerifyToken(token, "secret")
	if err == nil {
		fmt.Println("VULNERABLE")
		os.Exit(1)
	}
	fmt.Println("PATCHED")
}
"""
    try:
        with open(test_file_path, "w") as f:
            f.write(test_code)

        result = subprocess.run(
            ["go", "run", "server.go", "test_patch.go"],
            cwd="/home/user/app",
            capture_output=True,
            text=True
        )

        assert result.returncode == 0, f"Failed to compile/run server.go with test:\n{result.stderr}"
        assert "PATCHED" in result.stdout, "VerifyToken still accepts alg=none tokens without error."

    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)