# test_final_state.py

import os
import subprocess
import json
import tempfile
import time
import urllib.request
import urllib.error
import pytest

def test_nginx_upload():
    # Start services
    start_script = "/app/start_services.sh"
    if os.path.exists(start_script):
        subprocess.run([start_script], check=True)
        time.sleep(3) # Wait for services to be fully up

    # Generate a ~5MB CSV payload
    # 5MB = 5 * 1024 * 1024 bytes
    row = b"1,2021-01-01,100.00\n"
    num_rows = (5 * 1024 * 1024) // len(row)
    data = b"user_id,timestamp,transaction_amount\n" + (row * num_rows)

    req = urllib.request.Request("http://localhost:8080/upload", data=data, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK for 5MB upload, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Upload failed with HTTP {e.code}: {e.reason}. Nginx client_max_body_size might not be configured correctly.")
    except Exception as e:
        pytest.fail(f"Upload failed: {e}")

def test_csv_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/csv_sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer tool missing at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer tool at {sanitizer_path} is not executable"

    clean_dir = "/app/tests/corpus/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith(".csv")]
    assert len(clean_files) > 0, "No clean corpus files found"

    failed_clean = []

    for f in clean_files:
        input_path = os.path.join(clean_dir, f)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            output_path = tmp.name

        result = subprocess.run([sanitizer_path, input_path, output_path], capture_output=True)
        if result.returncode != 0:
            failed_clean.append(f"{f} (exit code {result.returncode})")
            continue

        try:
            with open(output_path, "r") as out_f:
                data = json.load(out_f)
            if not isinstance(data, list):
                failed_clean.append(f"{f} (output is not a JSON array)")
                continue
            if len(data) > 0:
                for item in data:
                    for key in ["user_id", "timestamp", "transaction_amount"]:
                        if key not in item:
                            failed_clean.append(f"{f} (missing key {key} in output)")
                            break
                    else:
                        continue
                    break
        except Exception as e:
            failed_clean.append(f"{f} (JSON parse error: {e})")

    if failed_clean:
        pytest.fail(f"{len(failed_clean)} of {len(clean_files)} clean modified/failed: {', '.join(failed_clean)}")

def test_csv_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/csv_sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer tool missing at {sanitizer_path}"

    evil_dir = "/app/tests/corpus/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith(".csv")]
    assert len(evil_files) > 0, "No evil corpus files found"

    failed_evil = []

    for f in evil_files:
        input_path = os.path.join(evil_dir, f)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            output_path = tmp.name

        result = subprocess.run([sanitizer_path, input_path, output_path], capture_output=True)
        if result.returncode == 0:
            failed_evil.append(f)

    if failed_evil:
        pytest.fail(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")