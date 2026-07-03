# test_final_state.py
import os
import subprocess
import time
import pytest

def test_compute_checksum():
    script = "/home/user/compute_checksum.sh"
    assert os.path.isfile(script), f"'{script}' does not exist."
    assert os.access(script, os.X_OK), f"'{script}' is not executable."

    # "abc" -> ascii 97, 98, 99. Sum = 294. Len = 3. 294 * 3 = 882. 882 % 256 = 114.
    result = subprocess.run([script, "abc"], capture_output=True, text=True)
    assert result.stdout.strip() == "114", f"compute_checksum.sh returned '{result.stdout.strip()}', expected '114'."

def test_makefile_and_compilation():
    makefile = "/home/user/Makefile"
    assert os.path.isfile(makefile), f"'{makefile}' does not exist."

    exe = "/home/user/api_client"
    if os.path.exists(exe):
        os.remove(exe)

    result = subprocess.run(["make", "client"], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"make client failed:\n{result.stderr}"
    assert os.path.isfile(exe), "Makefile did not build '/home/user/api_client'."

def test_c_client_memory_leak():
    exe = "/home/user/api_client"
    assert os.path.isfile(exe), f"'{exe}' not found. Cannot test memory leak."

    result = subprocess.run(
        ["valgrind", "--leak-check=full", exe, "verify"],
        capture_output=True, text=True
    )
    assert "definitely lost: 0 bytes" in result.stderr, "api_client.c still has a memory leak."

def test_valgrind_report():
    report = "/home/user/valgrind_report.txt"
    assert os.path.isfile(report), f"'{report}' does not exist."

    with open(report, "r") as f:
        content = f.read()

    assert "definitely lost: 0 bytes" in content, "valgrind_report.txt does not show 'definitely lost: 0 bytes'."

def test_mock_server_integration():
    server_script = "/home/user/mock_server.sh"
    assert os.path.isfile(server_script), f"'{server_script}' does not exist."
    assert os.access(server_script, os.X_OK), f"'{server_script}' is not executable."

    exe = "/home/user/api_client"
    assert os.path.isfile(exe), f"'{exe}' not found."

    server_proc = subprocess.Popen(
        [server_script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    time.sleep(1)  # Give the server a moment to start listening

    try:
        # "test" -> 116+101+115+116 = 448. Len = 4. 448 * 4 = 1792. 1792 % 256 = 0.
        result = subprocess.run([exe, "test"], capture_output=True, text=True, timeout=5)
        assert "CHECKSUM:0" in result.stdout, f"Client output does not contain 'CHECKSUM:0'. Got:\n{result.stdout}"
    finally:
        import signal
        os.killpg(os.getpgid(server_proc.pid), signal.SIGTERM)
        server_proc.wait(timeout=2)