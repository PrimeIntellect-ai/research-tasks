# test_final_state.py

import os
import subprocess
import json
import socket
import pytest

def test_process_backup_script_exists():
    script_path = "/home/user/process_backup.py"
    assert os.path.isfile(script_path), f"Expected Python script not found at {script_path}"

def test_port_forwarding_active():
    # Verify that something is listening on the Gateway Port (8111)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        result = s.connect_ex(('127.0.0.1', 8111))
        assert result == 0, "No service listening on Gateway Port 8111. Port forwarding is not functional."
    finally:
        s.close()

def test_archived_disk_qcow2_valid_and_compressed():
    target = "/home/user/archived_disk.qcow2"

    assert os.path.exists(target), f"Archived disk file not found at {target}"

    # Verify it is a valid qcow2 file
    res = subprocess.run(["qemu-img", "info", "--output=json", target], capture_output=True, text=True)
    assert res.returncode == 0, f"qemu-img info failed on {target}. Output: {res.stderr}"

    try:
        info = json.loads(res.stdout)
    except json.JSONDecodeError:
        pytest.fail("Failed to parse JSON output from qemu-img info")

    assert info.get('format') == 'qcow2', f"Expected format 'qcow2', but got {info.get('format')}"

    # Check virtual size is 50MB (52428800 bytes)
    expected_virtual_size = 52428800
    actual_virtual_size = info.get('virtual-size')
    assert actual_virtual_size == expected_virtual_size, f"Incorrect virtual size: expected {expected_virtual_size}, got {actual_virtual_size}"

    # Check physical file size for compression metric
    file_size = os.path.getsize(target)
    threshold = 2500000
    assert file_size <= threshold, f"Compression metric failed: file size {file_size} bytes is not <= {threshold} bytes. Did you use the compression flag?"