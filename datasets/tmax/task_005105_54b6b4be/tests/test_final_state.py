# test_final_state.py

import os
import subprocess
import random
import string
import datetime
import pytest
import urllib.request
import time

def test_dateparser_fixed():
    # Test if dateparser can be imported and works
    cmd = ["python3", "-c", "import dateparser; print(dateparser.parse('1 day ago'))"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to import and use dateparser. Output: {result.stderr}"
    assert "None" not in result.stdout, "dateparser returned None instead of a parsed date"

def test_nginx_setup_script():
    setup_script = "/home/user/setup_proxy.py"
    assert os.path.isfile(setup_script), f"Setup script {setup_script} is missing."

    # Run the setup script
    result = subprocess.run(["python3", setup_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Setup script failed: {result.stderr}"

    # Give nginx a moment to start
    time.sleep(1)

    # Check nginx.conf
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config {conf_path} is missing."
    with open(conf_path, "r") as f:
        conf_content = f.read()
    assert "proxy_pass http://unix:/tmp/backend_app.sock;" in conf_content, "Nginx config missing proxy_pass directive."

    # Check if nginx is listening on 8080
    # We can use ss or netstat, or just try to connect using urllib
    # Since there's no backend, it will return 502 Bad Gateway, but connection should succeed.
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        urllib.request.urlopen(req, timeout=2)
    except urllib.error.HTTPError as e:
        assert e.code in [502, 500, 404], f"Unexpected HTTP error: {e.code}"
    except Exception as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e}")

def generate_random_iso_timestamp():
    year = random.randint(1970, 2030)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    dt = datetime.datetime(year, month, day, hour, minute, second)
    iso = dt.isoformat()

    # Add timezone offset
    if random.choice([True, False]):
        iso += "Z"
    else:
        offset_h = random.randint(0, 12)
        offset_m = random.choice([0, 30, 45])
        sign = random.choice(["+", "-"])
        iso += f"{sign}{offset_h:02d}:{offset_m:02d}"
    return iso

def test_log_converter_fuzz_equivalence():
    agent_script = "/home/user/log_converter.py"
    oracle_bin = "/app/oracle/log_converter_oracle"

    assert os.path.isfile(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.isfile(oracle_bin), f"Oracle {oracle_bin} is missing."

    locales = ["en_US", "fr_FR", "es_ES", "ja_JP", "de_DE", "zh_CN", "ru_RU"]

    random.seed(42)
    inputs = []
    for _ in range(500):
        if random.random() < 0.1:
            # Invalid string
            ts = "".join(random.choices(string.ascii_letters + string.digits, k=15))
        else:
            ts = generate_random_iso_timestamp()
        loc = random.choice(locales)
        inputs.append((ts, loc))

    for ts, loc in inputs:
        # Run oracle
        oracle_res = subprocess.run([oracle_bin, ts, loc], capture_output=True, text=True)
        # Run agent
        agent_res = subprocess.run(["python3", agent_script, ts, loc], capture_output=True, text=True)

        assert oracle_res.returncode == agent_res.returncode, f"Return code mismatch on input {ts}, {loc}. Oracle: {oracle_res.returncode}, Agent: {agent_res.returncode}"
        assert oracle_res.stdout == agent_res.stdout, f"Stdout mismatch on input {ts}, {loc}.\nOracle: {oracle_res.stdout}\nAgent: {agent_res.stdout}"