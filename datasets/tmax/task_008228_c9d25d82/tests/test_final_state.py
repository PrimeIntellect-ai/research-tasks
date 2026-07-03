# test_final_state.py

import os
import time
import signal
import subprocess
import hashlib
import tarfile
import pytest

def test_watcher_executable_exists():
    """Test that the watcher executable exists and is executable."""
    assert os.path.isfile("/home/user/src/watcher.c"), "Source file /home/user/src/watcher.c does not exist."
    executable = "/home/user/bin/watcher"
    assert os.path.isfile(executable), f"Executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_watcher_behavior():
    """Run the watcher and verify its behavior with test files."""
    executable = "/home/user/bin/watcher"
    incoming_dir = "/home/user/incoming"
    backup_dir = "/home/user/backup"
    log_file = os.path.join(backup_dir, "watcher.log")
    tar_file = os.path.join(backup_dir, "master.tar")

    # Start watcher
    process = subprocess.Popen([executable], cwd=incoming_dir)
    time.sleep(1)  # Give it time to start and set up inotify

    assert process.poll() is None, "Watcher process exited prematurely."

    # Create test files
    test1_content = b"data set A\n"
    test2_content = b"data set B\n"
    test3_content = b"data set A\n"
    test4_content = b"ignore me\n"

    hash_a = hashlib.sha256(test1_content).hexdigest()
    hash_b = hashlib.sha256(test2_content).hexdigest()

    with open(os.path.join(incoming_dir, "test1.dat"), "wb") as f:
        f.write(test1_content)
    time.sleep(0.5)

    with open(os.path.join(incoming_dir, "test2.dat"), "wb") as f:
        f.write(test2_content)
    time.sleep(0.5)

    with open(os.path.join(incoming_dir, "test3.dat"), "wb") as f:
        f.write(test3_content)
    time.sleep(0.5)

    with open(os.path.join(incoming_dir, "test4.txt"), "wb") as f:
        f.write(test4_content)
    time.sleep(1)

    # Stop watcher gracefully
    process.send_signal(signal.SIGINT)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        pytest.fail("Watcher did not exit gracefully on SIGINT.")

    # Check log file
    assert os.path.isfile(log_file), f"Log file {log_file} was not created."
    with open(log_file, "r") as f:
        log_content = f.read()

    assert f"ADDED test1.dat {hash_a}" in log_content, "Log missing ADDED entry for test1.dat"
    assert f"ADDED test2.dat {hash_b}" in log_content, "Log missing ADDED entry for test2.dat"
    assert f"DUPLICATE test3.dat {hash_a}" in log_content, "Log missing DUPLICATE entry for test3.dat"
    assert "test4.txt" not in log_content, "Log contains entry for ignored file test4.txt"

    # Check tar file
    assert os.path.isfile(tar_file), f"Tar file {tar_file} was not created."
    try:
        with tarfile.open(tar_file, "r") as tar:
            names = tar.getnames()
            # Depending on how tar was invoked, paths might be relative or absolute.
            # We just check if the filename is in the tar contents.
            assert any(name.endswith("test1.dat") for name in names), "test1.dat not found in tar archive."
            assert any(name.endswith("test2.dat") for name in names), "test2.dat not found in tar archive."
            assert not any(name.endswith("test3.dat") for name in names), "duplicate test3.dat found in tar archive."
    except tarfile.TarError as e:
        pytest.fail(f"Failed to read tar archive {tar_file}: {e}")

    # Check if duplicate was deleted
    assert not os.path.exists(os.path.join(incoming_dir, "test3.dat")), "Duplicate file test3.dat was not deleted from incoming directory."