# test_final_state.py
import os
import random
import string
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import time
import pytest

def test_backup_name_gen_fuzz_equivalence():
    agent_bin = '/home/user/backup_name_gen'
    oracle_bin = '/app/oracle_gen'

    assert os.path.isfile(agent_bin), f"{agent_bin} does not exist."
    assert os.access(agent_bin, os.X_OK), f"{agent_bin} is not executable."

    random.seed(42)

    for _ in range(100):
        # Generate arg1: length 5-15 alphanumeric
        length = random.randint(5, 15)
        arg1 = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Generate arg2: YYYY-MM-DD
        year = random.randint(1990, 2030)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        arg2 = f"{year:04d}-{month:02d}-{day:02d}"

        # Run oracle
        oracle_proc = subprocess.run([oracle_bin, arg1, arg2], capture_output=True, text=True)
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run([agent_bin, arg1, arg2], capture_output=True, text=True)
        agent_out = agent_proc.stdout

        assert agent_out == oracle_out, (
            f"Output mismatch for inputs ('{arg1}', '{arg2}').\n"
            f"Expected: {oracle_out!r}\n"
            f"Got: {agent_out!r}"
        )

def test_submit_exp():
    script_path = '/home/user/submit.exp'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    proc = subprocess.run([script_path, 'test_service', '2023-01-01'], capture_output=True, text=True)
    assert proc.returncode == 0, "submit.exp failed to execute successfully."
    assert "Done" in proc.stdout, "submit.exp did not complete the interactive prompt successfully."

class MockBackendHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Backend OK")
    def log_message(self, format, *args):
        pass

def test_proxy():
    proxy_bin = '/home/user/proxy'
    assert os.path.isfile(proxy_bin), f"{proxy_bin} does not exist."
    assert os.access(proxy_bin, os.X_OK), f"{proxy_bin} is not executable."

    # Start mock backend
    server = HTTPServer(('127.0.0.1', 9090), MockBackendHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        time.sleep(0.5) # Give backend time to start

        # Send request to proxy
        req = urllib.request.Request('http://127.0.0.1:8080/')
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                body = response.read().decode('utf-8')
                assert response.status == 200
                assert body == "Backend OK", "Proxy did not return expected response from backend."
        except Exception as e:
            pytest.fail(f"Failed to connect to proxy or proxy failed to forward: {e}")
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()