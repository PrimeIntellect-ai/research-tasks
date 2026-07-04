# test_final_state.py

import os

def test_status_log_exists():
    """Check if the status.log file was created."""
    file_path = "/home/user/metrics_service/status.log"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run test_service.sh?"

def test_status_log_content():
    """Check if the status.log indicates all bugs were fixed."""
    file_path = "/home/user/metrics_service/status.log"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert "SUCCESS: ALL_BUGS_FIXED" in content, (
        f"Expected 'SUCCESS: ALL_BUGS_FIXED' in {file_path}, but found: '{content}'. "
        "Make sure all bugs (GCC linker, bc scale, array memory leak) are fixed correctly."
    )