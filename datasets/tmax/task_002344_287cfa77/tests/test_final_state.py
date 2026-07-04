# test_final_state.py

import os
import subprocess
import random
import string
import json
import urllib.request
import ssl
import pytest

def test_nginx_proxy():
    """Verify that Nginx is proxying /health over HTTPS on port 8443."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request("https://127.0.0.1:8443/health")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 OK, got {response.status}"
            # We don't strictly check the body, just that it successfully proxied and returned 200.
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx proxy on port 8443 or backend returned error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when testing Nginx proxy: {e}")

def test_parse_metrics_fuzz():
    """Fuzz test the parse_metrics script against an oracle implementation."""
    agent_script = "/home/user/parse_metrics"

    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script at {agent_script} is not executable"

    random.seed(42)

    for _ in range(100):
        num_pairs = random.randint(1, 10)
        pairs = []
        expected_data = {}
        for _ in range(num_pairs):
            k_len = random.randint(3, 8)
            v_len = random.randint(1, 10)
            k = ''.join(random.choices(string.ascii_lowercase, k=k_len))
            v = ''.join(random.choices(string.ascii_letters + string.digits, k=v_len))

            # Add random whitespace
            ws1 = ' ' * random.randint(0, 3)
            ws2 = ' ' * random.randint(0, 3)
            ws3 = ' ' * random.randint(0, 3)
            ws4 = ' ' * random.randint(0, 3)

            pair_str = f"{ws1}{k}{ws2}:{ws3}{v}{ws4}"
            pairs.append(pair_str)
            expected_data[k] = v

        # Join with commas and optional whitespace
        input_str = ""
        for i, p in enumerate(pairs):
            if i > 0:
                input_str += "," + (' ' * random.randint(0, 3))
            input_str += p

        expected_json = json.dumps({"data": expected_data}, separators=(',', ':'), sort_keys=True)

        try:
            proc = subprocess.run(
                [agent_script], 
                input=input_str.encode('utf-8'), 
                capture_output=True, 
                timeout=2
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on input: {input_str}")

        assert proc.returncode == 0, f"Agent script failed with return code {proc.returncode} on input: {input_str}\nStderr: {proc.stderr.decode('utf-8', errors='replace')}"

        agent_output = proc.stdout.decode('utf-8', errors='replace').strip()
        assert agent_output == expected_json, f"Mismatch on input: {input_str}\nExpected: {expected_json}\nGot: {agent_output}"