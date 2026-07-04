# test_final_state.py

import os
import re
import subprocess
import pytest
import urllib.request
import urllib.error

def test_nginx_config_updated():
    nginx_conf_path = "/home/user/app/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"File {nginx_conf_path} does not exist."
    with open(nginx_conf_path, "r") as f:
        content = f.read()
    assert "http://127.0.0.1:5000" in content, "Nginx config does not proxy to http://127.0.0.1:5000"

def test_settings_env_updated():
    settings_env_path = "/home/user/app/settings.env"
    assert os.path.isfile(settings_env_path), f"File {settings_env_path} does not exist."
    with open(settings_env_path, "r") as f:
        content = f.read()
    assert re.search(r"^REDIS_PORT=6379$", content, re.MULTILINE), "REDIS_PORT is not set to 6379 in settings.env"
    assert re.search(r"^FILTER_SCRIPT=/home/user/filter\.sh$", content, re.MULTILINE), "FILTER_SCRIPT is not set correctly in settings.env"

def test_filter_script_executable():
    script_path = "/home/user/filter.sh"
    assert os.path.isfile(script_path), f"Filter script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Filter script {script_path} is not executable."

def test_filter_script_against_clean_corpus():
    script_path = "/home/user/filter.sh"
    clean_corpus_path = "/home/user/corpora/clean/transactions.csv"
    assert os.path.isfile(clean_corpus_path), f"Clean corpus {clean_corpus_path} missing."

    with open(clean_corpus_path, "r") as f:
        clean_lines = f.read().splitlines()

    failed_lines = []
    for line in clean_lines:
        if not line.strip():
            continue
        process = subprocess.run(
            [script_path],
            input=(line + "\n").encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = process.stdout.decode("utf-8").strip()
        if output != line:
            failed_lines.append(line)

    if failed_lines:
        pytest.fail(f"{len(failed_lines)} of {len(clean_lines)} clean rows modified/rejected. Offending rows: {failed_lines[:5]}")

def test_filter_script_against_evil_corpus():
    script_path = "/home/user/filter.sh"
    evil_corpus_path = "/home/user/corpora/evil/anomalies.csv"
    assert os.path.isfile(evil_corpus_path), f"Evil corpus {evil_corpus_path} missing."

    with open(evil_corpus_path, "r") as f:
        evil_lines = f.read().splitlines()

    failed_lines = []
    for line in evil_lines:
        if not line.strip():
            continue
        process = subprocess.run(
            [script_path],
            input=(line + "\n").encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output = process.stdout.decode("utf-8").strip()
        if output != "":
            failed_lines.append(line)

    if failed_lines:
        pytest.fail(f"{len(failed_lines)} of {len(evil_lines)} evil rows bypassed. Offending rows: {failed_lines[:5]}")

def test_services_running():
    # Check if Nginx is listening on 8080
    try:
        req = urllib.request.Request("http://localhost:8080/")
        urllib.request.urlopen(req, timeout=2)
    except urllib.error.URLError as e:
        if isinstance(e.reason, ConnectionRefusedError):
            pytest.fail("Nginx is not listening on port 8080. Did you run start_services.sh?")
    except Exception:
        pass # Ignore other errors like 404, we just want to know if it's listening