# test_final_state.py

import os
import stat
import subprocess
import urllib.request
import urllib.error
import time
import pytest
import re

def test_nginx_config_fixed():
    config_path = "/app/nginx/nginx.conf"
    assert os.path.exists(config_path), f"Nginx config is missing at {config_path}"

    with open(config_path, 'r') as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:5000;" in content, "Nginx config should proxy to port 5000"

def test_env_file_fixed():
    env_path = "/app/c2/.env"
    assert os.path.exists(env_path), f"Environment file is missing at {env_path}"

    with open(env_path, 'r') as f:
        content = f.read()
    assert "REDIS_PASSWORD=Sup3rS3cr3tC2" in content, "The .env file should contain the correct REDIS_PASSWORD"

def test_keys_permissions():
    keys_dir = "/app/c2/keys"
    assert os.path.exists(keys_dir), f"Keys directory is missing at {keys_dir}"

    for filename in os.listdir(keys_dir):
        filepath = os.path.join(keys_dir, filename)
        if os.path.isfile(filepath):
            file_stat = os.stat(filepath)
            perms = stat.S_IMODE(file_stat.st_mode)
            assert perms == 0o600, f"Permissions for {filepath} should be 600, but are {oct(perms)}"

def test_end_to_end_flow():
    # Ensure the services are running by making a request
    # Since we can't guarantee start_infra.sh was run by the user in this test context,
    # we assume the environment is already running or we just test the endpoint.
    url = "http://127.0.0.1:8080/register?token=test_end_to_end"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx/Flask infrastructure: {e}")

    # Check Redis directly
    try:
        # Using redis-cli to check if the key exists
        result = subprocess.run(
            ["redis-cli", "-a", "Sup3rS3cr3tC2", "EXISTS", "session:test_end_to_end"],
            capture_output=True, text=True, check=True
        )
        assert result.stdout.strip() == "1", "The token was not saved to Redis correctly."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query Redis: {e}")

def test_c2_filter_script():
    script_path = "/home/user/c2_filter.sh"
    assert os.path.exists(script_path), f"Script missing at {script_path}"

    evil_corpus = "/app/corpora/blue_team_probes.txt"
    clean_corpus = "/app/corpora/valid_beacons.txt"

    evil_out = "/tmp/evil_out.txt"
    clean_out = "/tmp/clean_out.txt"

    # Run script on evil corpus
    result_evil = subprocess.run(["bash", script_path, evil_corpus, evil_out], capture_output=True, text=True)
    assert result_evil.returncode == 0, f"Script failed on evil corpus: {result_evil.stderr}"

    assert os.path.exists(evil_out), "Output file for evil corpus not created"
    with open(evil_out, 'r') as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    assert len(evil_lines) == 0, f"Expected 0 lines in evil output, but got {len(evil_lines)}. Bypassed probes: {evil_lines}"

    # Run script on clean corpus
    result_clean = subprocess.run(["bash", script_path, clean_corpus, clean_out], capture_output=True, text=True)
    assert result_clean.returncode == 0, f"Script failed on clean corpus: {result_clean.stderr}"

    assert os.path.exists(clean_out), "Output file for clean corpus not created"
    with open(clean_out, 'r') as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    with open(clean_corpus, 'r') as f:
        original_clean_lines = [line.strip() for line in f if line.strip()]

    assert len(clean_lines) == len(original_clean_lines), f"Expected {len(original_clean_lines)} lines in clean output, got {len(clean_lines)}"

    for orig, processed in zip(original_clean_lines, clean_lines):
        # We expect the token value to be replaced with [REDACTED]
        # e.g. /?action=poll&token=a1b2c3d4 -> /?action=poll&token=[REDACTED]
        expected = re.sub(r'token=[^&]+', 'token=[REDACTED]', orig)
        assert processed == expected, f"Clean line improperly modified. Expected: {expected}, Got: {processed}"