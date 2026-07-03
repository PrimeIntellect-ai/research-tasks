# test_final_state.py
import os
import subprocess
import socket
import hashlib
import requests
import json

def test_log_analysis_script():
    script_path = "/home/user/analyze_logs.sh"
    output_path = "/home/user/offline_nodes.txt"

    assert os.path.isfile(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    assert os.path.isfile(output_path), f"Missing output file: {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_content = "10.0.0.6 2023-10-12T10:00:00Z\n172.16.0.4 2023-10-12T10:10:00Z"
    assert content == expected_content, f"Output file content mismatch. Expected:\n{expected_content}\nGot:\n{content}"

def test_http_gateway():
    ip = "10.1.1.1"
    time = "999999"
    url = f"http://127.0.0.1:8080/sign?ip={ip}&time={time}"

    expected_hash = hashlib.md5(f"{ip}_SECRET-SRE-KEY_{time}".encode()).hexdigest()

    try:
        response = requests.get(url, timeout=2)
    except requests.RequestException as e:
        assert False, f"HTTP request to {url} failed: {e}"

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert data.get("ip") == ip, f"JSON 'ip' mismatch. Expected {ip}, got {data.get('ip')}"
    assert data.get("time") == time, f"JSON 'time' mismatch. Expected {time}, got {data.get('time')}"
    assert data.get("signature") == expected_hash, f"JSON 'signature' mismatch. Expected {expected_hash}, got {data.get('signature')}"

def test_tcp_gateway():
    ip = "192.168.2.2"
    time = "888888"
    payload = f"CHECK {ip} {time}\n".encode()

    expected_hash = hashlib.md5(f"{ip}_SECRET-SRE-KEY_{time}".encode()).hexdigest()
    expected_response = f"OK {expected_hash}\n".encode()

    try:
        with socket.create_connection(("127.0.0.1", 8081), timeout=2) as s:
            s.sendall(payload)
            response = s.recv(1024)
    except Exception as e:
        assert False, f"TCP connection/communication to 127.0.0.1:8081 failed: {e}"

    assert response == expected_response, f"TCP response mismatch. Expected {expected_response}, got {response}"