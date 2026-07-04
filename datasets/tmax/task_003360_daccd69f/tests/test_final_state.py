# test_final_state.py
import os
import subprocess
import random
import string
import urllib.request
import urllib.error
import pytest

def test_fuzz_transformer():
    oracle_path = "/home/user/oracle_transformer"
    agent_path = "/home/user/app/transformer"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    # Mixed ASCII (A-Z, a-z, 0-9, punctuation) plus some whitespace
    chars = string.ascii_letters + string.digits + string.punctuation + " \n\t"

    for _ in range(5000):
        length = random.randint(1, 1024)
        input_str = "".join(random.choices(chars, k=length))
        input_data = input_str.encode('utf-8')

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input {input_data!r}. "
            f"Expected {oracle_proc.returncode}, got {agent_proc.returncode}"
        )
        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input {input_data!r}.\n"
            f"Expected: {oracle_proc.stdout!r}\n"
            f"Got:      {agent_proc.stdout!r}"
        )

def test_end_to_end_nginx():
    random.seed(1337)
    chars = string.ascii_letters + string.digits + string.punctuation + " \n\t"

    for _ in range(10):
        length = random.randint(1, 100)
        input_data = "".join(random.choices(chars, k=length)).encode('utf-8')

        oracle_proc = subprocess.run(["/home/user/oracle_transformer"], input=input_data, capture_output=True)
        expected_output = oracle_proc.stdout

        req = urllib.request.Request("http://127.0.0.1:9090/transform", data=input_data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                body = response.read()
                assert body == expected_output, (
                    f"End-to-end output mismatch on input {input_data!r}.\n"
                    f"Expected: {expected_output!r}\n"
                    f"Got:      {body!r}"
                )
        except urllib.error.URLError as e:
            pytest.fail(f"Nginx end-to-end request failed: {e}")

def test_systemd_service():
    service_path = "/home/user/.config/systemd/user/backend.service"
    assert os.path.isfile(service_path), f"Systemd service file missing at {service_path}"

    with open(service_path, "r") as f:
        content = f.read()

    assert "TRANSFORMER_PATH=/home/user/app/transformer" in content, (
        "Missing or incorrect TRANSFORMER_PATH environment variable in systemd service file"
    )

def test_nginx_config():
    conf_path = "/home/user/app/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:8080;" in content or "proxy_pass http://localhost:8080;" in content, (
        "Nginx config proxy_pass not updated to forward to port 8080"
    )

def test_healthcheck_script_and_cron():
    script_path = "/home/user/app/healthcheck.sh"
    assert os.path.isfile(script_path), f"Healthcheck script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Healthcheck script at {script_path} is not executable"

    try:
        crontab_output = subprocess.check_output(["crontab", "-l", "-u", "user"], stderr=subprocess.STDOUT).decode('utf-8')
        assert "healthcheck.sh" in crontab_output, "Cron job for healthcheck.sh missing in user's crontab"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to get crontab for user 'user' or no crontab exists: {e.output.decode('utf-8')}")