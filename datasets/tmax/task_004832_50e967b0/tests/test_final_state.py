# test_final_state.py

import os
import subprocess
import json
import re
import socket
import time
import urllib.request
import pytest

def test_nginx_proxy():
    """
    Validates that Nginx is correctly configured to reverse-proxy to the Go API using mTLS.
    """
    # Check if Nginx is listening on 8080; if not, try to start/reload it.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8080))
    sock.close()

    if result != 0:
        subprocess.run(["nginx", "-c", "/app/nginx/nginx.conf"], check=False)
        time.sleep(1)  # Give Nginx a moment to start
    else:
        # Reload just in case the agent modified the config but didn't restart Nginx
        subprocess.run(["nginx", "-s", "reload", "-c", "/app/nginx/nginx.conf"], check=False)
        time.sleep(1)

    try:
        req = urllib.request.Request("http://127.0.0.1:8080/ping")
        with urllib.request.urlopen(req, timeout=3) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)
            assert data.get("status") == "ok", f"Expected status 'ok', got: {data}"
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx proxy or invalid response. Ensure Nginx proxies to the Go API with mTLS. Error: {e}")

def test_filter_evil_corpus():
    """
    Validates that the Go filter drops 100% of malicious logs.
    """
    evil_corpus = "/app/corpora/evil.jsonl"
    assert os.path.isfile(evil_corpus), f"Evil corpus missing at {evil_corpus}"

    cmd = f"go run /app/filter.go < {evil_corpus}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    assert result.returncode == 0, f"Go script failed to run on evil corpus: {result.stderr}"

    output_lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert len(output_lines) == 0, f"{len(output_lines)} evil logs bypassed the filter and were not dropped."

def test_filter_clean_corpus():
    """
    Validates that the Go filter preserves 100% of clean logs and properly redact sensitive data.
    """
    clean_corpus = "/app/corpora/clean.jsonl"
    assert os.path.isfile(clean_corpus), f"Clean corpus missing at {clean_corpus}"

    with open(clean_corpus, "r") as f:
        input_lines = [line for line in f.read().splitlines() if line.strip()]

    cmd = f"go run /app/filter.go < {clean_corpus}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    assert result.returncode == 0, f"Go script failed to run on clean corpus: {result.stderr}"

    output_lines = [line for line in result.stdout.splitlines() if line.strip()]

    assert len(output_lines) == len(input_lines), f"Expected {len(input_lines)} clean logs to be preserved, but got {len(output_lines)}. Clean logs were incorrectly dropped or added."

    unredacted_pattern = re.compile(r"CRED-[A-Z0-9]{4}-[A-Z0-9]{4}")
    redacted_pattern = re.compile(r"CRED-XXXX-XXXX")

    unredacted_occurrences_in_input = sum(len(unredacted_pattern.findall(line)) for line in input_lines)
    redacted_occurrences_in_output = sum(len(redacted_pattern.findall(line)) for line in output_lines)

    # Ensure no unredacted credentials remain in the output
    for i, line in enumerate(output_lines):
        assert not unredacted_pattern.search(line), f"Found unredacted CRED- pattern in preserved log line {i+1}."

    # Ensure the credentials were replaced with the exact string requested
    assert redacted_occurrences_in_output >= unredacted_occurrences_in_input, "Not all CRED- patterns were replaced with 'CRED-XXXX-XXXX'."