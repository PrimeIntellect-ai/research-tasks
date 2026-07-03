# test_final_state.py

import os
import subprocess
import pytest

def test_payload_exists():
    assert os.path.isfile("/home/user/payload.http"), "/home/user/payload.http is missing."

def test_rotated_password_exists_and_correct():
    path = "/home/user/rotated_password.txt"
    assert os.path.isfile(path), f"Exploit failed: {path} not found."
    with open(path, "r") as f:
        content = f.read()
    assert "ROTATED_OK_7739" in content, f"Exploit failed: incorrect content in {path}."

def test_fixed_code_compiles_and_mitigates():
    fixed_src = "/home/user/rotator_fixed.c"
    fixed_bin = "/home/user/rotator_fixed_bin"
    payload_file = "/home/user/payload.http"
    rotated_file = "/home/user/rotated_password.txt"

    assert os.path.isfile(fixed_src), f"Patch failed: {fixed_src} not found."

    # Compile the fixed code
    compile_result = subprocess.run(
        ["gcc", fixed_src, "-o", fixed_bin],
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"Patch failed: {fixed_src} does not compile.\n{compile_result.stderr}"

    # Remove the rotated password file if it exists
    if os.path.exists(rotated_file):
        os.remove(rotated_file)

    # Run the fixed binary with the payload
    with open(payload_file, "rb") as f:
        run_result = subprocess.run(
            [fixed_bin],
            stdin=f,
            capture_output=True
        )

    # Check that the rotated password file was NOT created
    assert not os.path.exists(rotated_file), "Patch failed: Fixed binary is still vulnerable (rotated_password.txt was created)."