# test_final_state.py

import os
import subprocess
import tempfile
import time
import socket
import json
import threading
import concurrent.futures
import pytest

def dummy_server(port, stop_event):
    """A simple TCP server that responds to HELLOTHERE with GENERALKENOBI."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', port))
    server.listen(1024)
    server.settimeout(0.1)
    while not stop_event.is_set():
        try:
            conn, addr = server.accept()
            conn.settimeout(1.0)
            data = conn.recv(1024)
            if b"HELLOTHERE" in data:
                conn.sendall(b"GENERALKENOBI")
            conn.close()
        except socket.timeout:
            continue
        except Exception:
            pass
    server.close()

def test_reverse_proxy_pipeline():
    git_dir = "/home/user/lb_sync.git"
    assert os.path.isdir(git_dir), f"Bare Git repository not found at {git_dir}"

    proxy_bin = "/home/user/rust_proxy/target/release/rust_proxy"
    assert os.path.isfile(proxy_bin), f"Rust proxy binary not found at {proxy_bin}. Did you run `cargo build --release`?"

    # Start dummy backend servers
    stop_event = threading.Event()
    t1 = threading.Thread(target=dummy_server, args=(9001, stop_event))
    t2 = threading.Thread(target=dummy_server, args=(9002, stop_event))
    t1.start()
    t2.start()

    proxy_proc = None

    try:
        # Push new configuration to trigger the pipeline
        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)

            routes = {"test1": 9001, "test2": 9002}
            with open(os.path.join(tmpdir, "routes.json"), "w") as f:
                json.dump(routes, f)

            subprocess.run(["git", "add", "routes.json"], cwd=tmpdir, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "update routes"], cwd=tmpdir, check=True, capture_output=True)

            push_proc = subprocess.run(["git", "push", git_dir, "master"], cwd=tmpdir, capture_output=True)
            assert push_proc.returncode == 0, f"Git push failed. post-receive hook might be failing. Stderr: {push_proc.stderr.decode()}"

        # Verify the pipeline extracted the config and updated the flag
        routes_path = "/home/user/lb_config/routes.json"
        flag_path = "/home/user/lb_config/reload_flag"

        assert os.path.isfile(routes_path), f"{routes_path} not found. The post-receive hook failed to checkout files."
        assert os.path.isfile(flag_path), f"{flag_path} not found. The expect script failed to run or reload the config."

        mtime = os.path.getmtime(flag_path)
        assert time.time() - mtime < 15, "reload_flag was not recently modified. The expect script did not successfully reload the config via the CLI."

        # Start the Rust proxy
        proxy_proc = subprocess.Popen([proxy_bin])
        time.sleep(1.5) # Wait for the proxy to bind and initialize

        # Blast the proxy with concurrent requests
        success_count = 0
        total_requests = 1000
        lock = threading.Lock()

        def send_request():
            nonlocal success_count
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2.0)
                s.connect(('127.0.0.1', 8080))
                s.sendall(b"ROUTE test1\nHELLOTHERE")
                resp = s.recv(1024)
                if b"GENERALKENOBI" in resp:
                    with lock:
                        success_count += 1
                s.close()
            except Exception:
                pass

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(send_request) for _ in range(total_requests)]
            concurrent.futures.wait(futures)

        success_rate = success_count / total_requests
        assert success_rate >= 0.95, f"Metric success_rate is {success_rate}, which is below the threshold of 0.95. The proxy may be dropping connections, not handling concurrency properly, or failing to route."

    finally:
        stop_event.set()
        t1.join()
        t2.join()
        if proxy_proc is not None:
            proxy_proc.terminate()
            proxy_proc.wait()