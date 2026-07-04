# test_final_state.py

import os
import subprocess
import csv
import json
import pytest
import tempfile
import urllib.request

SANITIZER_SCRIPT = "/home/user/data_pipeline/sanitizer.py"
EVIL_CORPUS_DIR = "/app/verifier/corpus/evil/"
CLEAN_CORPUS_DIR = "/app/verifier/corpus/clean/"
ENV_FILE = "/home/user/data_pipeline/.env"
NGINX_CONF = "/home/user/data_pipeline/nginx.conf"

def test_sanitizer_exists():
    assert os.path.isfile(SANITIZER_SCRIPT), f"Sanitizer script missing at {SANITIZER_SCRIPT}"

def run_sanitizer(input_path, output_path):
    result = subprocess.run(
        ["python3", SANITIZER_SCRIPT, input_path, output_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Sanitizer failed on {input_path}:\n{result.stderr}"

def test_adversarial_corpus_evil():
    if not os.path.isdir(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus directory {EVIL_CORPUS_DIR} not found.")

    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".csv")]
    bypassed_files = []

    for filename in evil_files:
        input_path = os.path.join(EVIL_CORPUS_DIR, filename)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            output_path = tmp.name

        try:
            run_sanitizer(input_path, output_path)

            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                rows = list(reader)

                # Should only contain header, or be completely empty
                if len(rows) > 1:
                    bypassed_files.append(filename)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the sanitizer: {', '.join(bypassed_files)}"

def test_adversarial_corpus_clean():
    if not os.path.isdir(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus directory {CLEAN_CORPUS_DIR} not found.")

    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".csv")]
    modified_files = []

    for filename in clean_files:
        input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
            output_path = tmp.name

        try:
            run_sanitizer(input_path, output_path)

            with open(input_path, "r", encoding="utf-8") as f1, open(output_path, "r", encoding="utf-8") as f2:
                in_rows = list(csv.reader(f1))
                out_rows = list(csv.reader(f2))

                if in_rows != out_rows:
                    modified_files.append(filename)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean files were modified by the sanitizer: {', '.join(modified_files)}"

def test_env_configuration():
    assert os.path.isfile(ENV_FILE), f".env file missing at {ENV_FILE}"

    with open(ENV_FILE, "r") as f:
        content = f.read()

    assert "REDIS_PORT=6379" in content, "REDIS_PORT is not correctly set in .env"
    assert "PG_PORT=5432" in content, "PG_PORT is not correctly set in .env"
    assert "MONGO_PORT=27017" in content, "MONGO_PORT is not correctly set in .env"

def test_nginx_configuration():
    assert os.path.isfile(NGINX_CONF), f"nginx.conf missing at {NGINX_CONF}"

    with open(NGINX_CONF, "r") as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:5000" in content.replace(" ", "").replace("/", ""), "Nginx configuration does not properly proxy to Flask API."

def test_e2e_script_success():
    e2e_script = "/home/user/data_pipeline/test_e2e.py"
    if os.path.isfile(e2e_script):
        result = subprocess.run(
            ["python3", e2e_script],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"End-to-End test script failed:\n{result.stdout}\n{result.stderr}"