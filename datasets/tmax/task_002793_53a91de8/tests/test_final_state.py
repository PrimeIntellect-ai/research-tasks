# test_final_state.py

import os
import subprocess
import pytest
import base64
import tempfile

def test_harden_ssh():
    script_path = "/home/user/harden_ssh.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("Port 22\nPasswordAuthentication yes\nPermitRootLogin prohibit-password\n")
        temp_config = f.name

    try:
        subprocess.run([script_path, temp_config], check=True)
        with open(temp_config, 'r') as f:
            content = f.read()
        assert "PasswordAuthentication no" in content, "PasswordAuthentication not set to no"
        assert "PermitRootLogin no" in content, "PermitRootLogin not set to no"
    finally:
        os.remove(temp_config)

def test_process_payload():
    cpp_path = "/home/user/process_payload.cpp"
    assert os.path.isfile(cpp_path), f"Missing C++ file: {cpp_path}"

    exe_path = "/home/user/process_payload"
    compile_cmd = ["g++", "-O2", cpp_path, "-o", exe_path, "-lcrypto", "-lssl"]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Compilation failed:\n{res.stderr}"

    payload_path = "/app/hidden_test_payload.enc"
    passphrase = "secure rotate alpha seven seven"
    out_file = "/home/user/rotation_plan.txt"

    if os.path.exists(out_file):
        os.remove(out_file)

    res = subprocess.run([exe_path, passphrase, payload_path], capture_output=True, text=True)
    assert res.returncode == 0, f"Execution failed:\n{res.stderr}"

    assert os.path.isfile(out_file), f"Output file not created: {out_file}"

    with open(out_file, 'r') as f:
        content = f.read().strip()

    assert "Allowed Subnet: 10.99.0.0/16" in content, "Incorrect or missing subnet in output"
    assert "Valid Certificates:" in content, "Missing 'Valid Certificates:' header"