# test_final_state.py
import os
import re
import subprocess
import socket
import time
import threading

def test_bashrc_timezone():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."
    with open(bashrc_path, "r") as f:
        content = f.read()

    # Look for export TZ=Asia/Tokyo with optional quotes
    pattern = re.compile(r"export\s+TZ=['\"]?Asia/Tokyo['\"]?")
    assert pattern.search(content) is not None, "TZ=Asia/Tokyo export not found in .bashrc"

def test_crontab():
    try:
        output = subprocess.check_output(["crontab", "-l", "-u", "user"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        output = ""

    # Check for * * * * * ... python3 /home/user/monitor.py
    pattern = re.compile(r"\*\s+\*\s+\*\s+\*\s+\*.*python3\s+/home/user/monitor\.py")
    assert pattern.search(output) is not None, "Crontab entry for monitor.py not found or incorrect."

def test_port_forward_script():
    script_path = "/home/user/port_forward.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Start a dummy server on 9090
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 9090))
    server.listen(1)

    def handle_client():
        try:
            conn, addr = server.accept()
            data = conn.recv(1024)
            if data == b"TEST":
                conn.sendall(b"SUCCESS")
            conn.close()
        except Exception:
            pass

    t = threading.Thread(target=handle_client)
    t.daemon = True
    t.start()

    # Start the port forwarder
    pf_proc = subprocess.Popen(["python3", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) # Wait for it to bind

    try:
        # Send data to 8080
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2)
        client.connect(('127.0.0.1', 8080))
        client.sendall(b"TEST")
        response = client.recv(1024)
        client.close()
        assert response == b"SUCCESS", "Port forwarder did not forward data correctly."
    finally:
        pf_proc.terminate()
        pf_proc.wait()
        server.close()

def test_monitor_script():
    monitor_path = "/home/user/monitor.py"
    assert os.path.isfile(monitor_path), f"{monitor_path} does not exist."

    # Ensure port_forward.py is not running
    subprocess.run(["pkill", "-f", "port_forward.py"])
    time.sleep(0.5)

    # Run monitor.py
    subprocess.run(["python3", monitor_path], check=True)
    time.sleep(1)

    # Check if port_forward.py is running
    try:
        output = subprocess.check_output(["pgrep", "-f", "port_forward.py"], text=True)
        assert output.strip() != "", "monitor.py did not start port_forward.py"
    except subprocess.CalledProcessError:
        assert False, "monitor.py did not start port_forward.py"
    finally:
        subprocess.run(["pkill", "-f", "port_forward.py"])