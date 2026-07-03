# test_final_state.py

import os
import stat
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

def test_lb_daemon_compiled_and_executable():
    """Check if /home/user/lb_daemon is compiled and executable."""
    path = "/home/user/lb_daemon"
    assert os.path.isfile(path), f"Executable {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_lb_daemon_behavior_no_conf():
    """Check that lb_daemon exits with code 2 and prints to stderr if UPSTREAM_CONF is not set."""
    path = "/home/user/lb_daemon"
    env = os.environ.copy()
    if "UPSTREAM_CONF" in env:
        del env["UPSTREAM_CONF"]

    process = subprocess.run([path], env=env, capture_output=True, text=True)
    assert process.returncode == 2, f"Expected exit code 2 when UPSTREAM_CONF is missing, got {process.returncode}."
    assert process.stderr.strip() != "", "Expected an error message on stderr when UPSTREAM_CONF is missing."

def test_lb_daemon_behavior_with_conf_and_port():
    """Check that lb_daemon reads LB_PORT and UPSTREAM_CONF correctly."""
    path = "/home/user/lb_daemon"
    conf_path = "/home/user/upstream.conf"

    # Ensure conf file exists so fopen doesn't crash if they didn't fix that part (though not required by prompt)
    if not os.path.exists(conf_path):
        with open(conf_path, "w") as f:
            f.write("dummy")

    # Test default port 8080
    env = os.environ.copy()
    env["UPSTREAM_CONF"] = conf_path
    if "LB_PORT" in env:
        del env["LB_PORT"]

    process = subprocess.run([path], env=env, capture_output=True, text=True)
    assert process.returncode == 0, f"Expected exit code 0, got {process.returncode}."
    assert "8080" in process.stdout, "Expected default port 8080 in output when LB_PORT is not set."

    # Test custom port
    env["LB_PORT"] = "9090"
    process = subprocess.run([path], env=env, capture_output=True, text=True)
    assert process.returncode == 0, f"Expected exit code 0, got {process.returncode}."
    assert "9090" in process.stdout, "Expected custom port 9090 in output when LB_PORT is set."

def test_upstream_conf_content():
    """Check if /home/user/upstream.conf contains the correct upstream ports."""
    path = "/home/user/upstream.conf"
    assert os.path.isfile(path), f"{path} is missing. The expect script might not have run successfully."

    with open(path, "r") as f:
        content = f.read()

    assert "upstream1:127.0.0.1:9001" in content, "Port 9001 missing for upstream 1."
    assert "upstream2:127.0.0.1:9002" in content, "Port 9002 missing for upstream 2."
    assert "upstream3:127.0.0.1:9003" in content, "Port 9003 missing for upstream 3."

def test_auto_init_exp_exists():
    """Check if /home/user/auto_init.exp exists."""
    path = "/home/user/auto_init.exp"
    assert os.path.isfile(path), f"{path} is missing."

def test_bash_profile_exports():
    """Check if /home/user/.bash_profile contains the required environment variables."""
    path = "/home/user/.bash_profile"
    assert os.path.isfile(path), f"{path} is missing."

    with open(path, "r") as f:
        content = f.read()

    assert "LB_PORT=8080" in content, "LB_PORT=8080 not found in .bash_profile"
    assert "UPSTREAM_CONF=/home/user/upstream.conf" in content, "UPSTREAM_CONF=/home/user/upstream.conf not found in .bash_profile"

class MockHealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            if self.server.return_200:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"ERROR")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def test_health_check_sh():
    """Test the health_check.sh script by mocking an HTTP server."""
    script_path = "/home/user/health_check.sh"
    log_path = "/home/user/health.log"

    assert os.path.isfile(script_path), f"{script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

    # Clear log file if it exists
    if os.path.exists(log_path):
        os.remove(log_path)

    # Start mock server
    server = HTTPServer(('127.0.0.1', 8080), MockHealthHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        # Test 1: Server returns 200
        server.return_200 = True
        subprocess.run([script_path], check=False)

        assert os.path.isfile(log_path), f"{log_path} was not created."
        with open(log_path, "r") as f:
            lines = f.readlines()
        assert len(lines) >= 1, "Log file is empty after successful request."
        assert lines[-1] == "UP\n", f"Expected 'UP\\n' in log, got {repr(lines[-1])}"

        # Test 2: Server returns 500
        server.return_200 = False
        subprocess.run([script_path], check=False)

        with open(log_path, "r") as f:
            lines = f.readlines()
        assert len(lines) >= 2, "Log file did not append after failed request."
        assert lines[-1] == "DOWN\n", f"Expected 'DOWN\\n' in log, got {repr(lines[-1])}"

    finally:
        server.shutdown()
        server.server_close()
        server_thread.join()

    # Test 3: Server is down (connection refused)
    subprocess.run([script_path], check=False)
    with open(log_path, "r") as f:
        lines = f.readlines()
    assert lines[-1] == "DOWN\n", f"Expected 'DOWN\\n' in log when server is unreachable, got {repr(lines[-1])}"