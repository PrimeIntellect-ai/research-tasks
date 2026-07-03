# test_final_state.py

import os
import subprocess
import time

WORKSPACE_DIR = "/home/user/workspace"

def test_investigation_txt():
    """Verify the contents of investigation.txt"""
    report_path = os.path.join(WORKSPACE_DIR, "investigation.txt")
    assert os.path.exists(report_path), f"Report file missing: {report_path}"

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, "investigation.txt must have at least 3 lines."
    assert "LD_LIBRARY_PATH" in lines[0], "Line 1 does not contain LD_LIBRARY_PATH"
    assert "/home/user/workspace/hidden_init.cfg" in lines[1], "Line 2 does not contain the correct absolute path"
    assert "std::domain_error" in lines[2], "Line 3 does not contain the correct exception type"

def test_hidden_init_cfg():
    """Verify the hidden_init.cfg file exists and contains ENABLE"""
    cfg_path = os.path.join(WORKSPACE_DIR, "hidden_init.cfg")
    assert os.path.exists(cfg_path), f"Configuration file missing: {cfg_path}"

    with open(cfg_path, "r") as f:
        content = f.read().strip()

    assert content == "ENABLE", f"Expected 'ENABLE' in {cfg_path}, found '{content}'"

def test_server_cpp_patched():
    """Verify that server.cpp has been patched to catch the exception and print the security message."""
    cpp_path = os.path.join(WORKSPACE_DIR, "server.cpp")
    assert os.path.exists(cpp_path), f"Source file missing: {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "[SECURITY] Caught malicious abort" in content, "server.cpp does not contain the required security print statement."
    assert "catch" in content, "server.cpp does not appear to catch the exception."

def test_server_and_client_execution():
    """Verify the server compiles, runs, and successfully handles the client payload without crashing."""
    # Compile the server
    make_result = subprocess.run(["make"], cwd=WORKSPACE_DIR, capture_output=True, text=True)
    assert make_result.returncode == 0, f"Failed to compile server:\n{make_result.stderr}"

    server_exe = os.path.join(WORKSPACE_DIR, "server")
    assert os.path.exists(server_exe), "Server binary not found after make."

    # Start the server with the correct LD_LIBRARY_PATH
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = os.path.join(WORKSPACE_DIR, "lib") + ":" + env.get("LD_LIBRARY_PATH", "")

    server_process = subprocess.Popen(
        [server_exe],
        cwd=WORKSPACE_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # Give the server a moment to start
        time.sleep(1)

        # Check if server died immediately
        assert server_process.poll() is None, "Server crashed or exited immediately upon startup."

        # Run the client
        client_result = subprocess.run(
            ["python3", "client.py"],
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True
        )

        assert client_result.returncode == 0, f"Client script failed:\n{client_result.stderr}"
        assert "All payloads processed successfully." in client_result.stdout, "Client did not complete all payloads successfully."

        # Ensure server is still running after client finishes
        assert server_process.poll() is None, "Server crashed during client execution."

    finally:
        # Cleanup server process
        server_process.terminate()
        server_process.wait(timeout=2)