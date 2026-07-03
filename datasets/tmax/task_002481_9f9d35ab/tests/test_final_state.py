# test_final_state.py

import os
import subprocess
import time
import pytest

def test_storage_dedup_executable_exists():
    executable = "/home/user/storage_dedup"
    assert os.path.exists(executable), f"Executable {executable} not found. Did you compile the C program?"
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_storage_dedup_behavior():
    watch_dir = "/home/user/watch_dir"
    archive_dir = "/home/user/archive_dir"
    config_file = "/home/user/config.txt"
    log_file = "/home/user/dedup.log"
    executable = "/home/user/storage_dedup"

    # Setup environment
    os.makedirs(watch_dir, exist_ok=True)
    os.makedirs(archive_dir, exist_ok=True)

    with open(config_file, "w") as f:
        f.write(f"WATCH_DIR={watch_dir}\n")
        f.write(f"ARCHIVE_DIR={archive_dir}\n")

    if os.path.exists(log_file):
        os.remove(log_file)

    # Start the daemon
    proc = subprocess.Popen([executable])
    time.sleep(1.0) # Wait for inotify initialization

    try:
        # 1. Create a new file
        with open(os.path.join(watch_dir, "test1.bin"), "w") as f:
            f.write("AAA")
        time.sleep(1.0)

        # 2. Create a duplicate file
        with open(os.path.join(watch_dir, "test2.bin"), "w") as f:
            f.write("AAA")
        time.sleep(1.0)

        # 3. Create another new file
        with open(os.path.join(watch_dir, "test3.bin"), "w") as f:
            f.write("BBB")
        time.sleep(1.0)

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()

    # Verification
    test1_watch = os.path.join(watch_dir, "test1.bin")
    test1_archive = os.path.join(archive_dir, "test1.bin")

    assert os.path.islink(test1_watch), "test1.bin in watch_dir should be a symlink for a new file."
    assert os.readlink(test1_watch) == test1_archive, "test1.bin symlink points to the wrong target."
    assert os.path.exists(test1_archive), "test1.bin was not moved to the archive_dir."

    test2_watch = os.path.join(watch_dir, "test2.bin")
    assert os.path.exists(test2_watch), "test2.bin is missing in watch_dir."
    assert not os.path.islink(test2_watch), "test2.bin should be a hard link, not a symlink."
    assert os.stat(test2_watch).st_ino == os.stat(test1_archive).st_ino, "test2.bin is not a hard link to test1.bin in the archive."

    test3_watch = os.path.join(watch_dir, "test3.bin")
    test3_archive = os.path.join(archive_dir, "test3.bin")
    assert os.path.islink(test3_watch), "test3.bin in watch_dir should be a symlink for a new file."
    assert os.readlink(test3_watch) == test3_archive, "test3.bin symlink points to the wrong target."
    assert os.path.exists(test3_archive), "test3.bin was not moved to the archive_dir."

    # Check logs
    assert os.path.exists(log_file), "/home/user/dedup.log was not created."
    with open(log_file, "r") as f:
        log_content = [line.strip() for line in f.readlines() if line.strip()]

    expected_logs = [
        "NEW: test1.bin -> test1.bin",
        "DUPLICATE: test2.bin -> test1.bin",
        "NEW: test3.bin -> test3.bin"
    ]

    for expected in expected_logs:
        assert expected in log_content, f"Expected log line '{expected}' not found in {log_file}."