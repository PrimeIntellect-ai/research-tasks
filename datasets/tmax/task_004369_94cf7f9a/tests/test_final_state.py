# test_final_state.py

import os
import subprocess
import pytest

def test_migration_log():
    log_path = "/home/user/migration.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "Migrated device 104 to status enum 2"
    assert content == expected_content, f"Log file content is incorrect. Expected: '{expected_content}', but got: '{content}'"

def test_output_binary_exists():
    out_path = "/home/user/data/output_v2.bin"
    assert os.path.isfile(out_path), f"Output binary {out_path} does not exist."
    assert os.path.getsize(out_path) > 0, f"Output binary {out_path} is empty."

def test_output_binary_content():
    out_path = "/home/user/data/output_v2.bin"
    schema_dir = "/home/user/schemas"
    v2_proto = "/home/user/schemas/v2.proto"

    # Use protoc to decode the binary
    cmd = [
        "protoc",
        "--decode=TelemetryV2",
        f"-I{schema_dir}",
        v2_proto
    ]

    try:
        with open(out_path, "rb") as f:
            result = subprocess.run(cmd, stdin=f, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to decode output binary using protoc. Error: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("protoc command not found. Cannot verify binary content.")

    output = result.stdout

    # Check for expected fields in the decoded text format
    assert "device_id: 104" in output, "device_id is incorrect or missing in output_v2.bin."
    assert "temperature: 42.5" in output, "temperature is incorrect or missing in output_v2.bin."
    assert "status: ERROR" in output, "status is incorrect or missing in output_v2.bin."
    assert "timestamp: 1710000000" in output, "timestamp is incorrect or missing in output_v2.bin."