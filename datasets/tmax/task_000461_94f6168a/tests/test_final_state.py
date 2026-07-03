# test_final_state.py
import os
import subprocess
import time
import urllib.request
import ssl
import threading
import smtpd
import asyncore

def test_deploy_script_exists():
    assert os.path.isfile("/home/user/deploy_edge.py"), "deploy_edge.py not found"

def test_run_deploy_script():
    result = subprocess.run(["/usr/bin/python3", "/home/user/deploy_edge.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy_edge.py failed: {result.stderr}"

    # Run again for idempotency
    result2 = subprocess.run(["/usr/bin/python3", "/home/user/deploy_edge.py"], capture_output=True, text=True)
    assert result2.returncode == 0, f"deploy_edge.py failed on second run: {result2.stderr}"

def test_directories_created():
    for d in ["/home/user/webroot", "/home/user/certs", "/home/user/bin"]:
        assert os.path.isdir(d), f"Directory {d} was not created"

def test_mock_sensor():
    sensor_path = "/home/user/bin/mock_sensor"
    assert os.path.isfile(sensor_path), "mock_sensor not found"
    assert os.access(sensor_path, os.X_OK), "mock_sensor is not executable"
    result = subprocess.run([sensor_path], capture_output=True, text=True)
    assert "TEMP=42.5C LOAD=1.2" in result.stdout, "mock_sensor output is incorrect"

def test_certificates():
    assert os.path.isfile("/home/user/certs/cert.pem"), "cert.pem not found"
    assert os.path.isfile("/home/user/certs/key.pem"), "key.pem not found"

def test_crontab():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    cron_entries = [line for line in lines if "/usr/bin/python3 /home/user/bin/collect.py" in line and not line.strip().startswith("#")]
    assert len(cron_entries) == 1, "Expected exactly one cron entry for collect.py"
    assert cron_entries[0].startswith("* * * * *"), "Cron entry does not run every minute"

def test_collector_execution():
    # Start a dummy SMTP server
    class DummySMTPServer(smtpd.SMTPServer):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.emails = []
        def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
            self.emails.append((mailfrom, rcpttos, data))

    smtp_server = DummySMTPServer(('127.0.0.1', 8025), None)
    t = threading.Thread(target=asyncore.loop, kwargs={'timeout': 1, 'use_poll': True})
    t.daemon = True
    t.start()

    try:
        # Run collect.py with empty environment
        result = subprocess.run(["env", "-i", "/usr/bin/python3", "/home/user/bin/collect.py"], capture_output=True, text=True)
        assert result.returncode == 0, f"collect.py failed with empty env: {result.stderr}"

        # Check metrics.html
        metrics_path = "/home/user/webroot/metrics.html"
        assert os.path.isfile(metrics_path), "metrics.html not found"
        with open(metrics_path, "r") as f:
            content = f.read()
        assert "<h1>TEMP=42.5C LOAD=1.2</h1>" in content, "metrics.html content is incorrect"

        # Check email
        assert len(smtp_server.emails) > 0, "No email was sent"
        mailfrom, rcpttos, data = smtp_server.emails[-1]
        assert "device@edge.local" in mailfrom, "Incorrect sender"
        assert "admin@edge.local" in rcpttos, "Incorrect recipient"
        data_str = data.decode('utf-8', errors='ignore')
        assert "Subject: Alert" in data_str, "Incorrect subject"
        assert "Metrics updated" in data_str, "Incorrect body"
    finally:
        smtp_server.close()

def test_web_server():
    # Start web server
    web_script = "/home/user/bin/start_web.sh"
    assert os.path.isfile(web_script), "start_web.sh not found"
    assert os.access(web_script, os.X_OK), "start_web.sh is not executable"

    proc = subprocess.Popen([web_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Wait for server to start

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request("https://127.0.0.1:8443/metrics.html")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, "Web server did not return 200 OK"
            content = response.read().decode('utf-8')
            assert "<h1>TEMP=42.5C LOAD=1.2</h1>" in content, "Web server returned incorrect content"
    finally:
        proc.terminate()
        proc.wait(timeout=5)