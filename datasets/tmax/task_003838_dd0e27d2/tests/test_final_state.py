# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import json
import socket
import pytest

def test_config_filter_corpus():
    """Test the Go CLI tool against the clean and evil corpora."""
    go_file = "/home/user/config_filter.go"
    assert os.path.exists(go_file), f"{go_file} does not exist"

    bin_path = "/tmp/config_filter_bin"
    compile_proc = subprocess.run(["go", "build", "-o", bin_path, go_file], capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Failed to compile {go_file}:\n{compile_proc.stderr}"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.json')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.json')]

    failed_clean = []
    for cf in clean_files:
        proc = subprocess.run([bin_path, cf], capture_output=True)
        if proc.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        proc = subprocess.run([bin_path, ef], capture_output=True)
        if proc.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    err_msg = []
    if failed_clean:
        err_msg.append(f"{len(failed_clean)} of {len(clean_files)} clean modified (rejected): {', '.join(failed_clean)}")
    if failed_evil:
        err_msg.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed (accepted): {', '.join(failed_evil)}")

    assert not failed_clean and not failed_evil, " | ".join(err_msg)

def test_e2e_nginx_redis():
    """Test the end-to-end flow via Nginx proxy to the Go server and Redis."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        assert s.connect_ex(('127.0.0.1', 8000)) == 0, "Nginx is not listening on 127.0.0.1:8000"
    finally:
        s.close()

    # We will use subprocess to call redis-cli to avoid external dependencies
    def get_redis_count():
        proc = subprocess.run(["redis-cli", "GET", "valid_configs_received"], capture_output=True, text=True)
        out = proc.stdout.strip()
        if out == "(nil)" or out == "":
            return 0
        try:
            return int(out)
        except ValueError:
            return 0

    initial_count = get_redis_count()

    clean_payload = json.dumps({
        "services": [
            {"service_name": "service_a", "allocated_ram_mb": 100.0, "cpu_shares": 5.0},
            {"service_name": "service_b", "allocated_ram_mb": 100.0, "cpu_shares": 5.0}
        ]
    }).encode('utf-8')

    evil_payload = json.dumps({
        "services": [
            {"service_name": "service_evil", "allocated_ram_mb": 1000000.0, "cpu_shares": 5.0}
        ]
    }).encode('utf-8')

    # Send clean payload
    req = urllib.request.Request("http://127.0.0.1:8000/ingest", data=clean_payload, method="POST", headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected HTTP 200 for clean payload, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Clean payload request failed with HTTP {e.code}")
    except Exception as e:
        pytest.fail(f"Clean payload request failed: {e}")

    # Check redis increment
    new_count = get_redis_count()
    assert new_count == initial_count + 1, "Redis counter 'valid_configs_received' was not incremented for clean payload"

    # Send evil payload
    req_evil = urllib.request.Request("http://127.0.0.1:8000/ingest", data=evil_payload, method="POST", headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req_evil) as response:
            pytest.fail(f"Expected HTTP 400 for evil payload, got {response.status}")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected HTTP 400 for evil payload, got {e.code}"
    except Exception as e:
        pytest.fail(f"Evil payload request failed unexpectedly: {e}")

    # Check redis not incremented
    final_count = get_redis_count()
    assert final_count == new_count, "Redis counter 'valid_configs_received' was incremented for evil payload"