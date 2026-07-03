# test_final_state.py

import os
import subprocess
import tempfile
import time
import urllib.request
import pytest
import redis
from bs4 import BeautifulSoup

def test_nginx_config_updated():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config not found at {conf_path}"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "listen 8080;" in content, "Nginx config not updated to listen on 8080"
    assert "root /home/user/reports;" in content, "Nginx config root not updated to /home/user/reports"

def test_log_tool_exists():
    tool_path = "/home/user/log_tool"
    assert os.path.isfile(tool_path), f"Executable not found at {tool_path}"
    assert os.access(tool_path, os.X_OK), f"File at {tool_path} is not executable"

def test_adversarial_corpus():
    tool_path = "/home/user/log_tool"
    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    clean_failed = []
    for f in os.listdir(clean_dir):
        if not f.endswith('.csv'): continue
        in_path = os.path.join(clean_dir, f)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as out_f:
            out_path = out_f.name

        subprocess.run([tool_path, "--filter", in_path, out_path], check=True)

        with open(in_path, "r") as inf, open(out_path, "r") as outf:
            in_lines = inf.readlines()
            out_lines = outf.readlines()

        if in_lines != out_lines:
            clean_failed.append(f)
        os.remove(out_path)

    evil_failed = []
    for f in os.listdir(evil_dir):
        if not f.endswith('.csv'): continue
        in_path = os.path.join(evil_dir, f)
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as out_f:
            out_path = out_f.name

        subprocess.run([tool_path, "--filter", in_path, out_path], check=True)

        with open(out_path, "r") as outf:
            out_lines = outf.readlines()

        # All lines in evil corpus contain malicious payloads, so output should be empty
        if len(out_lines) > 0:
            evil_failed.append(f)
        os.remove(out_path)

    assert not clean_failed, f"{len(clean_failed)} of {len(os.listdir(clean_dir))} clean modified/failed: {', '.join(clean_failed)}"
    assert not evil_failed, f"{len(evil_failed)} of {len(os.listdir(evil_dir))} evil bypassed: {', '.join(evil_failed)}"

def test_end_to_end_daemon():
    # Start services
    subprocess.run(["/app/start_services.sh"], check=True)
    time.sleep(2) # wait for redis and nginx to start

    # Start log_tool in daemon mode
    tool_proc = subprocess.Popen(["/home/user/log_tool", "--daemon"])
    time.sleep(1)

    try:
        # Inject synthetic records into Redis
        r = redis.Redis(host='localhost', port=6379, db=0)

        # Bucket 1: 1000000000 to 1000000059
        # Valid records
        r.lpush('raw_logs', '1000000010,sensor_B,20.0,ok')
        r.lpush('raw_logs', '1000000020,sensor_A,10.0,ok')
        r.lpush('raw_logs', '1000000030,sensor_C,30.0,ok')
        # Malicious record (should be ignored)
        r.lpush('raw_logs', '1000000040,sensor_D,40.0,<script>')

        # Trigger bucket finalization by sending a record for the next minute
        r.lpush('raw_logs', '1000000060,sensor_A,15.0,ok')

        # Wait for processing
        time.sleep(3)

        # Fetch HTML report
        req = urllib.request.Request("http://localhost:8080/index.html")
        try:
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8')
        except Exception as e:
            pytest.fail(f"Failed to fetch report from Nginx: {e}")

        soup = BeautifulSoup(html, 'html.parser')

        # Check bucket timestamp
        h1 = soup.find('h1')
        assert h1 is not None, "Missing <h1> tag in report"
        assert "1000000000" in h1.text or "1000000010" in h1.text, "Bucket timestamp not found in <h1>"

        # Check max/min temperatures
        p = soup.find('p')
        assert p is not None, "Missing <p> tag for temperatures"
        assert "30.0" in p.text, "Max temperature incorrect or missing"
        assert "10.0" in p.text, "Min temperature incorrect or missing"

        # Check sorted list of valid events
        ul = soup.find('ul')
        assert ul is not None, "Missing <ul> tag for events"
        lis = ul.find_all('li')
        assert len(lis) == 3, f"Expected 3 valid events in list, got {len(lis)}"

        assert "sensor_A" in lis[0].text, "First element should be sensor_A"
        assert "sensor_B" in lis[1].text, "Second element should be sensor_B"
        assert "sensor_C" in lis[2].text, "Third element should be sensor_C"

        assert "sensor_D" not in html, "Malicious record was not filtered out!"

    finally:
        tool_proc.terminate()
        tool_proc.wait()