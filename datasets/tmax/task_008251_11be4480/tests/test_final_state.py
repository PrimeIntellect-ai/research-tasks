# test_final_state.py
import os
import subprocess
import socket
import time
import threading

def test_ssh_key_injected():
    key_file = "/home/user/jwt_service/managed_authorized_keys"
    assert os.path.isfile(key_file), f"{key_file} does not exist."
    with open(key_file, "r") as f:
        content = f.read()
    expected_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPfakekeyhere admin@hack"
    assert expected_key in content, "The expected SSH key was not injected into managed_authorized_keys."

def test_exploit_token_saved():
    token_file = "/home/user/exploit_token.txt"
    assert os.path.isfile(token_file), f"{token_file} does not exist."
    with open(token_file, "r") as f:
        token = f.read().strip()

    parts = token.split('.')
    assert len(parts) >= 3, "The exploit token does not look like a valid JWT (missing dots)."

def test_scanner_exists_and_executable():
    scanner_path = "/home/user/vuln_scanner.sh"
    assert os.path.isfile(scanner_path), f"{scanner_path} does not exist."
    assert os.access(scanner_path, os.X_OK), f"{scanner_path} is not executable."

def test_scanner_output_secure_on_patched_server():
    scanner_path = "/home/user/vuln_scanner.sh"
    # Assuming the patched server is running on 8080
    result = subprocess.run([scanner_path, "localhost:8080"], capture_output=True, text=True)
    assert "SECURE" in result.stdout.strip(), "Scanner did not output 'SECURE' for the patched server on port 8080."

def test_scanner_output_vulnerable_on_original_server():
    # We need to run a dummy vulnerable server on port 8081 to test the scanner
    def run_vulnerable_server():
        server_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_fd.bind(('127.0.0.1', 8081))
        server_fd.listen(1)
        try:
            client_sock, _ = server_fd.accept()
            req = client_sock.recv(4096).decode()
            if "Authorization: Bearer " in req:
                # Naive mock of the vulnerability: always return 200 OK for any token
                response = "HTTP/1.1 200 OK\r\n\r\nSuccess"
            else:
                response = "HTTP/1.1 401 Unauthorized\r\n\r\n"
            client_sock.sendall(response.encode())
            client_sock.close()
        except:
            pass
        finally:
            server_fd.close()

    t = threading.Thread(target=run_vulnerable_server)
    t.daemon = True
    t.start()
    time.sleep(0.5) # Wait for server to start

    scanner_path = "/home/user/vuln_scanner.sh"
    result = subprocess.run([scanner_path, "localhost:8081"], capture_output=True, text=True)
    assert "VULNERABLE" in result.stdout.strip(), "Scanner did not output 'VULNERABLE' for the vulnerable server on port 8081."