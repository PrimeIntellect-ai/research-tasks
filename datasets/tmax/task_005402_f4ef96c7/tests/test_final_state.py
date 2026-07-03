# test_final_state.py
import os
import gzip
import json
import pytest

def test_script_exists():
    """Verify that the student wrote the automation script."""
    script_path = '/home/user/compact_logs.py'
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."

def test_filtered_file_exists_and_size():
    """Verify that the output file exists, is not empty, and meets the size threshold."""
    target_file = '/home/user/filtered.json.gz'
    assert os.path.exists(target_file), f"File {target_file} does not exist."

    size = os.path.getsize(target_file)
    assert size > 0, f"File {target_file} is empty."
    assert size <= 45000, f"File size {size} exceeds threshold 45000. Ensure you used maximum compression (compresslevel=9)."

def test_filtered_file_contents():
    """Verify that the output file is valid gzip, contains valid JSON, and has no DEBUG records."""
    target_file = '/home/user/filtered.json.gz'
    assert os.path.exists(target_file), f"File {target_file} does not exist."

    record_count = 0
    try:
        with gzip.open(target_file, 'rt') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                assert record.get("level") != "DEBUG", f"Found DEBUG record in output: {record}"
                record_count += 1
    except gzip.BadGzipFile:
        pytest.fail(f"File {target_file} is not a valid gzip archive.")
    except json.JSONDecodeError:
        pytest.fail(f"File {target_file} contains invalid JSON.")
    except Exception as e:
        pytest.fail(f"Failed to read or parse {target_file}: {e}")

    assert record_count > 0, "No records found in the filtered output."