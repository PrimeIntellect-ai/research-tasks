# test_final_state.py

import os
import subprocess
import random
import base64
import socket
import threading
import time
import pytest

def test_backup_script():
    backup_script = "/home/user/backup.sh"
    assert os.path.isfile(backup_script), f"Backup script not found: {backup_script}"
    assert os.access(backup_script, os.X_OK), f"Backup script is not executable: {backup_script}"

    # Run the backup script
    result = subprocess.run([backup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Backup script failed with exit code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    enc_file = "/home/user/configs_backup.tar.gz.enc"
    assert os.path.isfile(enc_file), f"Encrypted backup file not found: {enc_file}"

    # Decrypt the file
    decrypted_file = "/tmp/test_configs_backup.tar.gz"
    decrypt_cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-pass", "pass:8492",
        "-in", enc_file,
        "-out", decrypted_file
    ]
    decrypt_result = subprocess.run(decrypt_cmd, capture_output=True, text=True)
    assert decrypt_result.returncode == 0, f"Failed to decrypt backup file. Incorrect PIN or method?\nStderr: {decrypt_result.stderr}"

    # Verify it's a valid tarball
    tar_result = subprocess.run(["tar", "-tzf", decrypted_file], capture_output=True, text=True)
    assert tar_result.returncode == 0, "Decrypted file is not a valid gzip tarball."

def test_telemetry_parser_fuzz_equivalence():
    go_file = "/home/user/telemetry_parser.go"
    assert os.path.isfile(go_file), f"Go parser not found: {go_file}"

    ref_binary = "/app/bin/ref_parser"
    assert os.path.isfile(ref_binary), f"Reference binary not found: {ref_binary}"

    random.seed(42)
    for i in range(500):
        length = random.randint(8, 256)
        raw_bytes = bytes(random.getrandbits(8) for _ in range(length))
        b64_str = base64.b64encode(raw_bytes).decode('utf-8')

        # Run reference
        ref_result = subprocess.run([ref_binary, b64_str], capture_output=True, text=True)
        ref_out = ref_result.stdout

        # Run agent's Go program
        agent_result = subprocess.run(["go", "run", go_file, b64_str], capture_output=True, text=True)
        agent_out = agent_result.stdout

        assert agent_result.returncode == 0, f"Agent Go program failed on input {b64_str}\nStderr: {agent_result.stderr}"
        assert agent_out == ref_out, f"Mismatch on input: {b64_str}\nExpected: '{ref_out}'\nGot: '{agent_out}'"

def test_deploy_script():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deploy script not found: {deploy_script}"
    assert os.access(deploy_script, os.X_OK), f"Deploy script is not executable: {deploy_script}"

    # Run deploy script
    result = subprocess.run([deploy_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Deploy script failed with exit code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    for i in range(1, 6):
        node_dir = f"/home/user/edge_nodes/node_{i}"

        parser_path = os.path.join(node_dir, "telemetry_parser")
        assert os.path.isfile(parser_path), f"telemetry_parser executable missing in {node_dir}"
        assert os.access(parser_path, os.X_OK), f"telemetry_parser in {node_dir} is not executable"

        log_path = os.path.join(node_dir, "deploy.log")
        assert os.path.isfile(log_path), f"deploy.log missing in {node_dir}"

        with open(log_path, "r") as f:
            log_content = f.read().strip()

        assert log_content == "Deployment successful", f"Unexpected content in {log_path}: '{log_content}'"

def test_port_forwarding():
    # Start a dummy server on port 8081
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind(('127.0.0.1', 8081))
        server.listen(1)
    except Exception as e:
        pytest.fail(f"Could not bind to port 8081 to test forwarding: {e}")

    received_data = []

    def server_thread():
        try:
            server.settimeout(5.0)
            conn, addr = server.accept()
            conn.settimeout(2.0)
            data = conn.recv(1024)
            received_data.append(data)
            conn.close()
        except Exception:
            pass

    t = threading.Thread(target=server_thread)
    t.start()

    time.sleep(0.5) # Give server time to start accepting

    test_message = b"PING_FROM_TEST\n"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(2.0)
    try:
        client.connect(('127.0.0.1', 8080))
        client.sendall(test_message)
        client.close()
    except Exception as e:
        server.close()
        t.join()
        pytest.fail(f"Failed to connect and send data to port 8080: {e}")

    t.join()
    server.close()

    assert len(received_data) == 1, "No data received on port 8081. Port forwarding is not working."
    assert received_data[0] == test_message, f"Data mismatch. Expected {test_message}, got {received_data[0]}"