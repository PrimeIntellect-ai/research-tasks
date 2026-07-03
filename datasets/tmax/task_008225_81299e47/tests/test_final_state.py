# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE = "/home/user/minilogd_project"
REPORT_FILE = "/home/user/e2e_report.txt"
E2E_SCRIPT = os.path.join(WORKSPACE, "run_e2e.sh")
TEST_PROTOCOL = os.path.join(WORKSPACE, "test_protocol.c")
MAKEFILE = os.path.join(WORKSPACE, "Makefile")

def test_e2e_report():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."
    with open(REPORT_FILE, "r") as f:
        content = f.read().strip()
    assert content == "E2E_STATUS: SUCCESS", f"Expected 'E2E_STATUS: SUCCESS' in {REPORT_FILE}, got '{content}'"

def test_test_protocol_exists():
    assert os.path.isfile(TEST_PROTOCOL), f"Unit test file {TEST_PROTOCOL} does not exist."

def test_makefile_has_test_target():
    assert os.path.isfile(MAKEFILE), f"Makefile {MAKEFILE} does not exist."
    with open(MAKEFILE, "r") as f:
        content = f.read()
    assert "test:" in content, "Makefile does not contain a 'test' target."

def test_e2e_script_executable():
    assert os.path.isfile(E2E_SCRIPT), f"Orchestration script {E2E_SCRIPT} does not exist."
    assert os.access(E2E_SCRIPT, os.X_OK), f"Orchestration script {E2E_SCRIPT} is not executable."

def test_valgrind_memory_leaks():
    # Build the project
    build_proc = subprocess.run(
        ["make", "clean", "all"],
        cwd=WORKSPACE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert build_proc.returncode == 0, f"Failed to build project:\n{build_proc.stderr.decode()}"

    # Run valgrind on minilogd in background
    valgrind_cmd = [
        "valgrind",
        "--leak-check=full",
        "--error-exitcode=1",
        "./minilogd",
        "8081"
    ]
    server_proc = subprocess.Popen(
        valgrind_cmd,
        cwd=WORKSPACE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    import time
    time.sleep(1) # Wait for server to start

    # Send message and QUIT
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 8081))
        s.sendall(b"MSG:TEST_VALGRIND\n")
        s.close()

        time.sleep(0.5)

        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect(("127.0.0.1", 8081))
        s2.sendall(b"QUIT\n")
        s2.close()
    except Exception as e:
        server_proc.kill()
        pytest.fail(f"Failed to communicate with minilogd: {e}")

    stdout, stderr = server_proc.communicate(timeout=5)

    assert server_proc.returncode == 0, f"Valgrind reported errors or leaks (exit code {server_proc.returncode}):\n{stderr.decode()}"