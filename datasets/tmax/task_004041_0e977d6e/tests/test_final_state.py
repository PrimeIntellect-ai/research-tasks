# test_final_state.py

import os
import tarfile
import json
import subprocess
import urllib.request
import urllib.error
import time
import pytest

def test_phase1_backup():
    backup_path = "/home/user/history_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup tarball {backup_path} is missing."

    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            assert len(names) > 0, "Backup tarball is empty."
    except tarfile.ReadError:
        pytest.fail(f"File {backup_path} is not a valid gzip-compressed tarball.")

def test_phase2_api_binding():
    api_path = "/app/services/api/app.py"
    assert os.path.isfile(api_path), f"File {api_path} is missing."
    with open(api_path, "r") as f:
        content = f.read()
    assert "0.0.0.0" not in content, "The Capacity API is still binding to 0.0.0.0."
    assert "127.0.0.1" in content, "The Capacity API must bind to 127.0.0.1."

def test_phase2_nginx_proxy():
    nginx_path = "/app/services/nginx/nginx.conf"
    assert os.path.isfile(nginx_path), f"File {nginx_path} is missing."
    with open(nginx_path, "r") as f:
        content = f.read()
    assert "proxy_pass" in content, "nginx.conf is missing proxy_pass directive."
    assert "127.0.0.1:5000" in content or "localhost:5000" in content, "nginx.conf is not proxying to the API on port 5000."

def test_phase2_end_to_end_flow():
    # Attempt to start services just in case they aren't running
    start_script = "/app/services/start_all.sh"
    if os.path.isfile(start_script) and os.access(start_script, os.X_OK):
        subprocess.run([start_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2)  # Give services a moment to start

    payload = json.dumps({"host":"web-01","cpu_percent":45.5,"mem_bytes":1024}).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8080/ingest", data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.getcode() == 200, f"Expected HTTP 200, got {response.getcode()}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to reach the ingestion endpoint through Nginx: {e}")

    # Check Redis queue
    result = subprocess.run(['redis-cli', 'LPOP', 'capacity_queue'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to execute redis-cli."
    output = result.stdout.strip()
    assert "web-01" in output, "The payload was not found in the Redis capacity_queue."

def test_phase3_sanitizer_evil_corpus():
    script_path = "/home/user/sanitizer.py"
    evil_corpus = "/app/corpora/evil/evil_logs.jsonl"

    assert os.path.isfile(script_path), f"Sanitizer script {script_path} is missing."
    assert os.path.isfile(evil_corpus), f"Evil corpus {evil_corpus} is missing."

    with open(evil_corpus, "r") as f:
        evil_data = f.read()

    result = subprocess.run(
        ["python3", script_path],
        input=evil_data,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Sanitizer script crashed on evil corpus: {result.stderr}"

    output_lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert len(output_lines) == 0, f"{len(output_lines)} evil logs bypassed the sanitizer."

def test_phase3_sanitizer_clean_corpus():
    script_path = "/home/user/sanitizer.py"
    clean_corpus = "/app/corpora/clean/clean_logs.jsonl"

    assert os.path.isfile(script_path), f"Sanitizer script {script_path} is missing."
    assert os.path.isfile(clean_corpus), f"Clean corpus {clean_corpus} is missing."

    with open(clean_corpus, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    clean_data = "\n".join(clean_lines) + "\n"

    result = subprocess.run(
        ["python3", script_path],
        input=clean_data,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Sanitizer script crashed on clean corpus: {result.stderr}"

    output_lines = [line for line in result.stdout.splitlines() if line.strip()]

    missing_count = len(clean_lines) - len(output_lines)
    assert len(output_lines) == len(clean_lines), f"{missing_count} of {len(clean_lines)} clean logs modified or dropped."

    for i, out_line in enumerate(output_lines):
        try:
            parsed = json.loads(out_line)
            expected = json.loads(clean_lines[i])
            assert parsed == expected, f"Clean log modified. Expected {expected}, got {parsed}"
        except json.JSONDecodeError:
            pytest.fail("Sanitizer output is not valid JSON.")