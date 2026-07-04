# test_final_state.py
import os
import socket
import hashlib
import subprocess
import time
import pytest

def send_to_server(payload: str, host: str = '127.0.0.1', port: int = 8080) -> str:
    """Send a payload to the TCP server and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((host, port))
        s.sendall(payload.encode('utf-8'))
        s.shutdown(socket.SHUT_WR)

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    return response.decode('utf-8').strip()

def get_redis_key(key: str) -> str:
    """Get a value from Redis using redis-cli."""
    result = subprocess.run(
        ['redis-cli', 'GET', key],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_c_binary_compiled():
    """Verify that the math_eval binary was compiled and is executable."""
    binary_path = "/app/math_eval/math_eval"
    assert os.path.isfile(binary_path), f"Binary {binary_path} does not exist. Makefile might not have run correctly."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_server_script_exists():
    """Verify that server.sh exists and is executable."""
    script_path = "/app/server.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_server_listening():
    """Verify that the server is listening on port 8080."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "TCP server is not listening on 127.0.0.1:8080"

def test_rpn_evaluation_and_caching():
    """Verify that the server correctly evaluates RPN and caches the result."""
    payload = "PUSH 5\nPUSH 7\nADD\nPUSH 2\nMUL\nPRINT\n"
    expected_result = "24"

    # First request
    response1 = send_to_server(payload)
    assert response1 == expected_result, f"Expected output '{expected_result}', got '{response1}'"

    # Verify caching in Redis
    # Calculate MD5 of payload ignoring trailing whitespace
    stripped_payload = payload.rstrip()
    md5_hash = hashlib.md5(stripped_payload.encode('utf-8')).hexdigest()

    redis_val = get_redis_key(md5_hash)
    assert redis_val == expected_result, f"Redis cache miss or incorrect value. Expected '{expected_result}', got '{redis_val}'"

    # Second request (should hit cache)
    response2 = send_to_server(payload)
    assert response2 == expected_result, f"Expected output from cache '{expected_result}', got '{response2}'"

def test_stack_overflow_handling():
    """Verify that the C backend handles pushing many items (memory safety fix)."""
    # Push 200 items, which should exceed a typical hardcoded small stack (e.g., 100)
    payload_lines = [f"PUSH {i}" for i in range(200)]
    payload_lines.append("PRINT")
    payload = "\n".join(payload_lines) + "\n"

    expected_result = "199"

    response = send_to_server(payload)
    assert response == expected_result, f"Expected output '{expected_result}' after pushing 200 items, got '{response}'. The C backend might have crashed due to stack overflow."