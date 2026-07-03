# test_final_state.py
import os
import socket
import subprocess
import time

def test_makefile_fixed():
    # Verify the Makefile or compilation process works
    # The binary should be compiled and running, but let's check if it can be built
    result = subprocess.run(["make"], cwd="/app/vendored_kv", capture_output=True, text=True)
    assert result.returncode == 0, f"Make failed: {result.stderr}"

def test_wal_recovered():
    wal_path = "/app/data/server.wal"
    assert os.path.isfile(wal_path), "WAL file is missing."
    with open(wal_path, "r") as f:
        content = f.read()
    assert "4 SET corrupted_key" not in content, "Corrupted line still present in WAL file."

def test_repro_script_exists():
    script_path = "/home/user/repro.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK) or "bash" in open(script_path).read(), "repro.sh should be executable or a bash script."

def get_process_rss(port):
    # Find PID listening on the port
    try:
        output = subprocess.check_output(["lsof", "-t", f"-i:{port}"]).decode().strip()
        pids = output.split('\n')
        if not pids or not pids[0]:
            return None
        pid = pids[0]
        # Get RSS in KB
        ps_output = subprocess.check_output(["ps", "-o", "rss=", "-p", pid]).decode().strip()
        return int(ps_output)
    except Exception:
        return None

def test_server_protocol_and_memory_leak():
    host = "127.0.0.1"
    port = 9090

    # Wait a bit for the server to be available if needed, though it should already be running
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5.0)
    try:
        s.connect((host, port))
    except Exception as e:
        assert False, f"Failed to connect to {host}:{port}: {e}"

    # Test AUTH
    s.sendall(b"AUTH b34r3r_s3cr3t\n")
    resp = s.recv(1024)
    assert resp == b"OK\n", f"Expected OK\\n for AUTH, got {resp}"

    # Test GET from WAL
    s.sendall(b"GET app_name\n")
    resp = s.recv(1024)
    assert resp == b"VALUE kv_server\n", f"Expected VALUE kv_server\\n, got {resp}"

    # Test SET and GET
    s.sendall(b"SET test_mem leak_test\n")
    resp = s.recv(1024)
    assert resp == b"OK\n", f"Expected OK\\n for SET, got {resp}"

    # Memory leak check
    initial_rss = get_process_rss(port)
    assert initial_rss is not None, "Could not determine RSS of the server process."

    # Send 10,000 GET requests
    for _ in range(10000):
        s.sendall(b"GET test_mem\n")
        resp = s.recv(1024)
        if resp != b"VALUE leak_test\n":
            assert False, f"Unexpected response during memory leak test: {resp}"

    final_rss = get_process_rss(port)
    assert final_rss is not None, "Could not determine RSS of the server process after requests."

    rss_diff_kb = final_rss - initial_rss
    # 1MB is 1024 KB
    assert rss_diff_kb < 1024, f"Memory leak detected: RSS grew by {rss_diff_kb} KB (limit 1024 KB)."

    s.close()