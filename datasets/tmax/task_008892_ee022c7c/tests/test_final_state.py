# test_final_state.py

import os
import re

def test_restored_data_exists_and_size():
    """Test that the restored data file exists and has the correct size."""
    file_path = "/home/user/restore_dir/restored_data.bin"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The legacy tool may not have run successfully."

    file_size = os.path.getsize(file_path)
    assert file_size == 512000, f"Expected file size 512000, but got {file_size}. The legacy tool may not have run correctly."

def test_metrics_log_exists_and_format():
    """Test that the metrics log exists and has the correct format and values."""
    log_path = "/home/user/restore_metrics.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    before_match = re.search(r"^Before:\s+(\d+)\s+bytes", content, re.MULTILINE)
    after_match = re.search(r"^After:\s+(\d+)\s+bytes", content, re.MULTILINE)

    assert before_match is not None, "Log file does not contain the 'Before: <bytes> bytes' line."
    assert after_match is not None, "Log file does not contain the 'After: <bytes> bytes' line."

    before_bytes = int(before_match.group(1))
    after_bytes = int(after_match.group(1))

    # The legacy tool creates a 512000 byte file. The directory size difference should be exactly 512000.
    expected_after = before_bytes + 512000
    assert after_bytes == expected_after, f"Expected After bytes to be {expected_after} (Before + 512000), but got {after_bytes}."

def test_automation_script_exists():
    """Test that the automation script exists."""
    sh_exists = os.path.isfile("/home/user/run_restore.sh")
    py_exists = os.path.isfile("/home/user/run_restore.py")
    assert sh_exists or py_exists, "Automation script /home/user/run_restore.sh or .py does not exist."