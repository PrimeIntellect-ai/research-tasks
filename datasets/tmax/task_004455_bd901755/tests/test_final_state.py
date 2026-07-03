# test_final_state.py

import os
import subprocess
import time
import socket
import pytest

def test_init_mount_script():
    script_path = "/home/user/init_mount.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run the script twice to test idempotency
    for i in range(2):
        result = subprocess.run([script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Run {i+1} of {script_path} failed with exit code {result.returncode}. stderr: {result.stderr}"

    data_file = "/home/user/mock_mount/data.bin"
    assert os.path.exists(data_file), f"Data file {data_file} does not exist."
    assert os.path.getsize(data_file) == 4096, f"Data file {data_file} is not exactly 4096 bytes."

def test_custom_fstab():
    fstab_path = "/home/user/custom_fstab"
    assert os.path.exists(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    expected_content = "/dev/loop0 /home/user/mock_mount ext4 defaults 0 0"
    assert content == expected_content, f"Content of {fstab_path} is incorrect. Expected '{expected_content}', got '{content}'."

def test_systemd_service():
    service_path = "/home/user/capacity-exporter.service"
    assert os.path.exists(service_path), f"Service file {service_path} does not exist."

    with open(service_path, "r") as f:
        content = f.read()

    assert "ExecStart=/home/user/capacity_monitor/target/release/capacity_monitor" in content, "ExecStart directive is missing or incorrect."
    assert "WantedBy=default.target" in content, "WantedBy directive is missing or incorrect."

    # After directive check
    # It might be one line `After=network-online.target mount-prep.service` or multiple lines
    assert "network-online.target" in content and "mount-prep.service" in content, "After directive does not contain required targets."
    lines = content.split('\n')
    after_lines = [line for line in lines if line.strip().startswith("After=")]
    assert after_lines, "No After= directive found."
    combined_after = " ".join(after_lines)
    assert "network-online.target" in combined_after, "network-online.target missing from After="
    assert "mount-prep.service" in combined_after, "mount-prep.service missing from After="

def test_rust_exporter():
    cargo_dir = "/home/user/capacity_monitor"
    assert os.path.exists(os.path.join(cargo_dir, "Cargo.toml")), "Cargo.toml does not exist in the expected directory."

    # Build the project
    build_result = subprocess.run(["cargo", "build", "--release"], cwd=cargo_dir, capture_output=True, text=True)
    assert build_result.returncode == 0, f"Cargo build failed. stderr: {build_result.stderr}"

    binary_path = os.path.join(cargo_dir, "target/release/capacity_monitor")
    assert os.path.exists(binary_path), f"Compiled binary not found at {binary_path}."

    # Run the binary
    process = subprocess.Popen([binary_path])
    try:
        # Give it a moment to start listening
        time.sleep(1)

        # Connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("127.0.0.1", 9090))

        data = s.recv(1024).decode("utf-8")
        s.close()

        assert data == "BYTES:4096\n", f"Expected 'BYTES:4096\\n', got '{data}'"
    finally:
        process.terminate()
        process.wait()