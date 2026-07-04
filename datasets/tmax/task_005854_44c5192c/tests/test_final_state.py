# test_final_state.py
import os
import subprocess
import time

def test_daemon_executable():
    """Check if the daemon executable exists and is executable."""
    daemon_path = "/home/user/doc_daemon"
    assert os.path.exists(daemon_path), f"Daemon executable not found at {daemon_path}"
    assert os.access(daemon_path, os.X_OK), f"Daemon at {daemon_path} is not executable"

def test_daemon_behavior():
    """Start the daemon, drop a log file, and verify the binary archive."""
    daemon_path = "/home/user/doc_daemon"
    watch_dir = "/home/user/doc_watch"
    archive_path = "/home/user/doc_archive.bin"

    # Ensure watch directory exists
    os.makedirs(watch_dir, exist_ok=True)

    # Clean up any existing archive from previous runs or manual testing
    if os.path.exists(archive_path):
        os.remove(archive_path)

    # Start the daemon
    process = subprocess.Popen([daemon_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Give the watcher time to initialize
        time.sleep(1)

        # Drop a test file
        test_file = os.path.join(watch_dir, "test1.txt")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Some random chatter.\n")
            f.write(">>>DOC: Auth Setup\n")
            f.write("Use OAuth2.\n")
            f.write("Token in header.\n")
            f.write("<<<END\n")
            f.write("Garbage text.\n")

        # Give the daemon time to process the file
        time.sleep(2)
    finally:
        # Terminate the daemon
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()

    # Verify the archive was created
    assert os.path.exists(archive_path), f"Archive file {archive_path} was not created by the daemon"

    # Read and verify the archive contents
    with open(archive_path, "rb") as f:
        data = f.read()

    expected_magic = b"DOC1"
    expected_title = b"Auth Setup"
    expected_title_len = bytes([len(expected_title)])
    expected_content = b"Use OAuth2.\nToken in header."
    expected_content_len = len(expected_content).to_bytes(4, byteorder="little")

    expected_data = expected_magic + expected_title_len + expected_title + expected_content_len + expected_content

    assert data == expected_data, f"Archive data mismatch.\nExpected: {expected_data.hex()}\nGot:      {data.hex()}"

def test_source_code_locking():
    """Verify that a file locking mechanism is used in the source code."""
    workspace_dir = "/home/user/workspace/doc_aggregator"
    assert os.path.exists(workspace_dir), f"Workspace directory {workspace_dir} not found"

    found_lock = False
    lock_keywords = ["lock_exclusive", "flock", "try_lock_exclusive", "lock"]

    for root, _, files in os.walk(workspace_dir):
        for file in files:
            if file.endswith(".rs"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if any(keyword in content for keyword in lock_keywords):
                        found_lock = True
                        break
        if found_lock:
            break

    assert found_lock, "Could not find any standard file locking mechanism (e.g., lock_exclusive, flock) in the Rust source code."