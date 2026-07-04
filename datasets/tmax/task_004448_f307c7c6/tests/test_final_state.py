# test_final_state.py

import os
import subprocess
import tempfile
import stat

def test_rust_library_built():
    so_path = "/home/user/rust_lib/target/release/librust_lib.so"
    assert os.path.isfile(so_path), f"Rust shared library not found at {so_path}"

def test_bash_script_exists_and_executable():
    script_path = "/home/user/run_client.sh"
    assert os.path.isfile(script_path), f"Bash script not found at {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Bash script at {script_path} is not executable"

def test_grpc_server_and_client_integration():
    script_path = "/home/user/run_client.sh"

    # Create a test payload
    payload = b"hello world"
    expected_checksum = sum(payload) % 65536

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(payload)
        tmp_path = tmp.name

    try:
        # Run the client script
        result = subprocess.run([script_path, tmp_path], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"Client script failed with return code {result.returncode}. Stderr: {result.stderr}"

        output = result.stdout.strip()
        assert output == str(expected_checksum), f"Expected checksum {expected_checksum}, but got {output}"

    finally:
        os.remove(tmp_path)

def test_grpc_server_and_client_integration_random():
    script_path = "/home/user/run_client.sh"

    # Create another test payload with different bytes
    payload = os.urandom(1024)
    expected_checksum = sum(payload) % 65536

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(payload)
        tmp_path = tmp.name

    try:
        # Run the client script
        result = subprocess.run([script_path, tmp_path], capture_output=True, text=True, timeout=10)
        assert result.returncode == 0, f"Client script failed with return code {result.returncode}. Stderr: {result.stderr}"

        output = result.stdout.strip()
        assert output == str(expected_checksum), f"Expected checksum {expected_checksum}, but got {output}"

    finally:
        os.remove(tmp_path)