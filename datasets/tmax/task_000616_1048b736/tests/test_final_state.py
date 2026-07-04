# test_final_state.py
import os
import ssl
import socket
import time
import subprocess
import pytest

SSH_DIR = '/home/user/.ssh'
PRIV_KEY = os.path.join(SSH_DIR, 'redteam_key')
PUB_KEY = os.path.join(SSH_DIR, 'redteam_key.pub')
TLS_DIR = '/home/user/tls'
CERT_FILE = os.path.join(TLS_DIR, 'cert.pem')
KEY_FILE = os.path.join(TLS_DIR, 'key.pem')
SERVER_SCRIPT = '/home/user/server.py'

def test_ssh_keys_exist():
    """Verify that the generated SSH keys exist."""
    assert os.path.isfile(PRIV_KEY), f"Private key not found at {PRIV_KEY}"
    assert os.path.isfile(PUB_KEY), f"Public key not found at {PUB_KEY}"

def test_tls_certs_exist():
    """Verify that the TLS certificate and private key exist."""
    assert os.path.isfile(CERT_FILE), f"Certificate not found at {CERT_FILE}"
    assert os.path.isfile(KEY_FILE), f"Private key not found at {KEY_FILE}"

def test_server_script_exists():
    """Verify that the server script exists."""
    assert os.path.isfile(SERVER_SCRIPT), f"Server script not found at {SERVER_SCRIPT}"

def test_payload_delivery_and_decryption():
    """
    Start the server, connect via TLS, verify the certificate CN,
    receive the payload, and verify it decrypts to the expected bash command.
    """
    # Read the public key to construct the expected command
    with open(PUB_KEY, 'r') as f:
        pub_key_content = f.read()

    expected_command = f'echo "{pub_key_content}" >> /home/user/authorized_keys'

    # Start the server
    proc = subprocess.Popen(
        ["python3", SERVER_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Prepare SSL context, trusting the generated self-signed cert
        context = ssl.create_default_context(cafile=CERT_FILE)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_REQUIRED

        # Attempt to connect with retries
        connected = False
        sock = None
        for _ in range(5):
            if proc.poll() is not None:
                stdout, stderr = proc.communicate()
                pytest.fail(f"Server script exited prematurely. Return code: {proc.returncode}\nStderr: {stderr.decode('utf-8', errors='ignore')}")
            try:
                sock = socket.create_connection(('127.0.0.1', 8443), timeout=3)
                connected = True
                break
            except (ConnectionRefusedError, OSError):
                time.sleep(1)

        if not connected:
            pytest.fail("Could not connect to server on 127.0.0.1:8443 after 5 seconds.")

        data = b""
        cert = None
        try:
            with sock:
                with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
                    cert = ssock.getpeercert()
                    while True:
                        chunk = ssock.recv(4096)
                        if not chunk:
                            break
                        data += chunk
        except Exception as e:
            pytest.fail(f"Failed to communicate over TLS or retrieve data: {e}")

        assert cert is not None, "Failed to retrieve peer certificate."

        # Verify Certificate Common Name (CN)
        cn_found = False
        for rdn in cert.get('subject', ()):
            for attr in rdn:
                if attr[0] == 'commonName' and attr[1] == 'redteam':
                    cn_found = True
                    break
        assert cn_found, f"Certificate Common Name (CN) is not 'redteam'. Subject found: {cert.get('subject')}"

        assert len(data) > 0, "No data received from the server."
        assert len(data) % 4 == 0, f"Received payload length ({len(data)}) is not a multiple of 4."

        # Decrypt data
        key = b'\xDE\xAD\xBE\xEF'
        decrypted = bytearray()
        for i in range(0, len(data), 4):
            chunk = data[i:i+4]
            # Reverse bytes
            chunk = chunk[::-1]
            # XOR with key
            for j in range(4):
                decrypted.append(chunk[j] ^ key[j])

        # Strip null padding and decode
        try:
            decrypted_str = decrypted.rstrip(b'\x00').decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("Decrypted payload could not be decoded as UTF-8. Encryption/Decryption logic may be flawed.")

        assert decrypted_str == expected_command, (
            f"Decrypted payload does not match expected command.\n"
            f"Expected: {expected_command}\n"
            f"Got: {decrypted_str}"
        )

    finally:
        # Cleanup server process
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()