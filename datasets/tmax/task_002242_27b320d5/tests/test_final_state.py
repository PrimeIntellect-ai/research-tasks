# test_final_state.py
import os
import time
import struct
import hashlib
import urllib.request
import subprocess
import pytest

def get_expected_hash(backup_path):
    h = hashlib.sha256()
    with open(backup_path, 'rb') as f:
        while True:
            len_bytes = f.read(4)
            if not len_bytes:
                break
            if len(len_bytes) < 4:
                pytest.fail("Incomplete length header in backup.dat")
            L = struct.unpack('<I', len_bytes)[0]
            data = f.read(L)
            if len(data) < L:
                pytest.fail("Incomplete data chunk in backup.dat")
            h.update(data)
    return h.hexdigest()

def test_restore_tool_performance_and_correctness():
    tool_path = '/home/user/bin/restore_tool'
    backup_path = '/home/user/data/backup.dat'
    out_path = '/home/user/restore_out/recovered.bin'

    assert os.path.isfile(tool_path), f"Compiled tool not found at {tool_path}"
    assert os.path.isfile(backup_path), f"Backup data not found at {backup_path}"

    # Remove output file if it exists to ensure a fresh run
    if os.path.exists(out_path):
        os.remove(out_path)

    expected_hash = get_expected_hash(backup_path)

    # Run the tool and measure execution time
    start_time = time.perf_counter()
    try:
        subprocess.run([tool_path, backup_path, out_path], check=True, timeout=5)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Tool execution failed: {e}")
    except subprocess.TimeoutExpired:
        pytest.fail("Tool execution timed out after 5 seconds.")

    execution_time = time.perf_counter() - start_time

    # Assert performance metric
    assert execution_time <= 0.20, f"Execution time {execution_time:.4f}s exceeded threshold of 0.20s"

    # Verify the local file was created
    assert os.path.isfile(out_path), f"Output file {out_path} was not created."

    # Verify via Nginx
    url = 'http://127.0.0.1:8080/recovered.bin'
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            file_data = response.read()
    except Exception as e:
        pytest.fail(f"Failed to fetch {url} via Nginx: {e}")

    # Verify checksum
    actual_hash = hashlib.sha256(file_data).hexdigest()
    assert actual_hash == expected_hash, "SHA256 checksum of the recovered file does not match the expected raw data."

def test_email_alert_sent():
    log_path = '/home/user/mail.log'
    assert os.path.isfile(log_path), f"Mail log not found at {log_path}"

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        log_content = f.read()

    assert "Restore Complete" in log_content, "The subject 'Restore Complete' was not found in the mail log."
    assert "backup-admin@local" in log_content, "The recipient 'backup-admin@local' was not found in the mail log."