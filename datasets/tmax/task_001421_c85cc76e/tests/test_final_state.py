# test_final_state.py

import json
import socket
import pytest
import requests
import math

def test_network_stats_endpoint():
    url = "http://127.0.0.1:8080/api/v1/network-stats"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the agent's service at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "slope" in data, "Missing 'slope' in JSON response"
    assert "intercept" in data, "Missing 'intercept' in JSON response"
    assert "max_degree" in data, "Missing 'max_degree' in JSON response"

    # Expected values
    expected_slope = -0.5333
    expected_intercept = 4.6
    expected_max_degree = 5

    assert math.isclose(data["slope"], expected_slope, abs_tol=0.001), \
        f"Expected slope around {expected_slope}, got {data['slope']}"
    assert math.isclose(data["intercept"], expected_intercept, abs_tol=0.001), \
        f"Expected intercept around {expected_intercept}, got {data['intercept']}"
    assert data["max_degree"] == expected_max_degree, \
        f"Expected max_degree {expected_max_degree}, got {data['max_degree']}"


def test_redis_cache_updated():
    # Connect to Redis via socket to avoid needing the 'redis' pip package
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(('127.0.0.1', 6379))
    except Exception as e:
        pytest.fail(f"Failed to connect to Redis on 127.0.0.1:6379. Is it running? Error: {e}")

    # Send GET command using RESP protocol
    key = "dna_raw_reads"
    cmd = f"*2\r\n$3\r\nGET\r\n${len(key)}\r\n{key}\r\n"
    s.sendall(cmd.encode('utf-8'))

    resp = b""
    while True:
        chunk = s.recv(4096)
        resp += chunk
        if len(chunk) < 4096:
            break
    s.close()

    resp_str = resp.decode('utf-8', errors='ignore')

    # RESP bulk string format for GET: $<length>\r\n<data>\r\n
    # If key doesn't exist, it returns $-1\r\n
    assert resp_str.startswith("$"), f"Unexpected Redis response: {resp_str}"
    if resp_str.startswith("$-1"):
        pytest.fail("Key 'dna_raw_reads' does not exist in Redis.")

    # Extract the data part
    parts = resp_str.split("\r\n", 2)
    if len(parts) >= 2:
        data_str = parts[1]
    else:
        pytest.fail("Failed to parse Redis response.")

    try:
        cached_reads = json.loads(data_str)
    except json.JSONDecodeError:
        pytest.fail(f"Data in Redis is not valid JSON. Data: {data_str}")

    expected_reads = [
        "ATGCGTA", "TGCGTAC", "CGTACGA", "AAAAAAT", 
        "TTTTTTT", "ATGCGGG", "GGGGGGG", "AAAAAAG",
        "ATGC", "CGTA"
    ]
    assert cached_reads == expected_reads, \
        f"Cached reads in Redis do not match expected reads. Got: {cached_reads}"