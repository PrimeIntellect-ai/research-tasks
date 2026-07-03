# test_final_state.py

import os
import time
import subprocess
import urllib.request
import urllib.error
import threading
import json

def get_rss_bytes(pid):
    """Read the VmRSS (Resident Set Size) in bytes for a given PID."""
    try:
        with open(f"/proc/{pid}/status", "r") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    # VmRSS is in kB
                    return int(line.split()[1]) * 1024
    except Exception:
        pass
    return 0

def get_listening_port(pid):
    """Find the listening port for the given PID by parsing /proc/net/tcp."""
    import re
    try:
        # Get inodes for the process's sockets
        inodes = set()
        for fd in os.listdir(f"/proc/{pid}/fd"):
            try:
                link = os.readlink(f"/proc/{pid}/fd/{fd}")
                if link.startswith("socket:[") and link.endswith("]"):
                    inodes.add(link[8:-1])
            except OSError:
                continue

        # Find the port matching the inode in /proc/net/tcp
        with open("/proc/net/tcp", "r") as f:
            for line in f.readlines()[1:]:
                parts = line.strip().split()
                if len(parts) >= 10:
                    local_addr = parts[1]
                    state = parts[3]
                    inode = parts[9]
                    if state == "0A" and inode in inodes:  # 0A is TCP_LISTEN
                        port_hex = local_addr.split(":")[1]
                        return int(port_hex, 16)
    except Exception:
        pass
    return None

def test_math_service_memory_leak():
    binary_path = "/home/user/math-service-fixed"

    assert os.path.exists(binary_path), f"Binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable"

    # Start the service
    process = subprocess.Popen(
        [binary_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Wait for the service to start and listen on a port
        port = None
        for _ in range(50):
            port = get_listening_port(process.pid)
            if port is not None:
                break
            time.sleep(0.1)
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                pytest.fail(f"Service crashed immediately. STDOUT: {stdout} STDERR: {stderr}")

        # Fallback to 8080 if we couldn't detect it, though it might fail
        if port is None:
            port = 8080

        # Load generation and memory monitoring
        max_rss = 0
        requests_sent = 0
        target_requests = 50000
        start_time = time.time()

        # We will run for a maximum of 15 seconds or until 50k requests are sent
        while requests_sent < target_requests and (time.time() - start_time) < 15:
            try:
                # Send request to /factorize
                # Using a changing number to ensure caching logic is exercised
                req_url = f"http://localhost:{port}/factorize?number={1000000 + requests_sent}"
                req = urllib.request.Request(req_url)
                with urllib.request.urlopen(req, timeout=1) as response:
                    response.read()
            except urllib.error.URLError:
                pass # Ignore errors, we just want to push load

            requests_sent += 1

            # Sample memory every 100 requests
            if requests_sent % 100 == 0:
                current_rss = get_rss_bytes(process.pid)
                if current_rss > max_rss:
                    max_rss = current_rss

                # Fail early if we significantly exceed the threshold
                if max_rss > 60 * 1024 * 1024:
                    break

        # Final memory check
        current_rss = get_rss_bytes(process.pid)
        if current_rss > max_rss:
            max_rss = current_rss

        max_rss_mb = max_rss / (1024 * 1024)
        threshold_mb = 50.0

        assert max_rss_mb <= threshold_mb, (
            f"Memory leak detected! Maximum RSS was {max_rss_mb:.2f} MB, "
            f"which exceeds the threshold of {threshold_mb} MB."
        )

    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()