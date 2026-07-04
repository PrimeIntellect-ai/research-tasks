# test_final_state.py

import os
import time
import tarfile
import pytest
import subprocess

def trigger_shutdown_and_wait():
    shutdown_file = "/home/user/incoming/SHUTDOWN"
    with open(shutdown_file, "w") as f:
        f.write("")

    # Wait up to 5 seconds for the curator.py process to exit
    for _ in range(10):
        # Check if python3 /home/user/curator.py is running
        try:
            output = subprocess.check_output(["pgrep", "-f", "curator.py"]).decode()
            if not output.strip():
                break
        except subprocess.CalledProcessError:
            # pgrep returns non-zero if no processes matched
            break
        time.sleep(0.5)

@pytest.fixture(scope="session", autouse=True)
def setup_shutdown():
    trigger_shutdown_and_wait()

def test_curated_archives_exist_and_valid():
    """Test that the curated tar.gz files exist and contain the correct safe files."""
    curated_dir = "/home/user/curated"

    archive1 = os.path.join(curated_dir, "build_v1.tar.gz")
    assert os.path.isfile(archive1), f"{archive1} is missing."

    with tarfile.open(archive1, "r:gz") as tar:
        names = tar.getnames()
        assert "safe1.txt" in names, "safe1.txt missing from build_v1.tar.gz"
        assert "dir/safe2.txt" in names, "dir/safe2.txt missing from build_v1.tar.gz"
        assert not any("escape" in name for name in names), "Malicious file escape.txt found in build_v1.tar.gz"
        assert not any("absolute" in name for name in names), "Malicious file absolute.txt found in build_v1.tar.gz"

    archive2 = os.path.join(curated_dir, "build_v2.tar.gz")
    assert os.path.isfile(archive2), f"{archive2} is missing."

    with tarfile.open(archive2, "r:gz") as tar:
        names = tar.getnames()
        assert "config.json" in names, "config.json missing from build_v2.tar.gz"

def test_incoming_directory_cleaned():
    """Test that the original zip files are removed from incoming."""
    incoming_dir = "/home/user/incoming"
    files = os.listdir(incoming_dir)
    assert "build_v1.zip" not in files, "build_v1.zip was not deleted from incoming directory."
    assert "build_v2.zip" not in files, "build_v2.zip was not deleted from incoming directory."
    assert "SHUTDOWN" in files, "SHUTDOWN file is missing from incoming directory."

def test_log_contents():
    """Test that the log file contains the correct output."""
    log_file = "/home/user/logs/curator.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    with open(log_file, "r") as f:
        log_contents = f.read()

    expected_lines = [
        "Processed build_v1.zip: 2 safe, 2 malicious",
        "Processed build_v2.zip: 1 safe, 0 malicious"
    ]

    for line in expected_lines:
        assert line in log_contents, f"Expected log line '{line}' not found in {log_file}."