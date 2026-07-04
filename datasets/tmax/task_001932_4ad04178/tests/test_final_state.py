# test_final_state.py

import os
import time
import socket
import json
import subprocess
import pytest

APP_DIR = "/home/user/app"

def test_deploy_script_exists_and_executable():
    deploy_script = os.path.join(APP_DIR, "deploy.sh")
    assert os.path.isfile(deploy_script), f"Deployment script {deploy_script} is missing."
    assert os.access(deploy_script, os.X_OK), f"Deployment script {deploy_script} is not executable."

def test_processor_binary_compiled():
    # Run the deployment script to ensure everything is compiled and started
    deploy_script = os.path.join(APP_DIR, "deploy.sh")
    try:
        subprocess.run([deploy_script], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"deploy.sh failed to run. stdout: {e.stdout}, stderr: {e.stderr}")

    processor_bin = os.path.join(APP_DIR, "processor_bin")
    assert os.path.isfile(processor_bin), f"Compiled binary {processor_bin} is missing."
    assert os.access(processor_bin, os.X_OK), f"Compiled binary {processor_bin} is not executable."

def test_supervisord_conf_updated():
    conf_path = os.path.join(APP_DIR, "supervisord.conf")
    assert os.path.isfile(conf_path), f"Configuration file {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for autorestart=true (case-insensitive check could be better, but standard is fine)
    assert "autorestart=true" in content.lower(), "supervisord.conf does not contain autorestart=true for the processor."

def test_throughput_metric():
    # Wait for services to settle and process some logs
    # The aggregator takes 3 seconds to bind, so wait 8 seconds total
    time.sleep(8)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect(("127.0.0.1", 9002))
        s.sendall(b"STATS\n")
        data = s.recv(4096).decode("utf-8").strip()
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to aggregator on port 9002 or retrieve stats: {e}")

    try:
        stats = json.loads(data)
    except json.JSONDecodeError:
        pytest.fail(f"Aggregator returned invalid JSON: {data}")

    assert "total_processed" in stats, "Aggregator stats missing 'total_processed'"
    assert "uptime_seconds" in stats, "Aggregator stats missing 'uptime_seconds'"

    total_processed = stats["total_processed"]
    uptime_seconds = stats["uptime_seconds"]

    assert uptime_seconds > 0, "Aggregator uptime is 0, cannot calculate throughput."

    throughput = total_processed / uptime_seconds
    threshold = 50000

    assert throughput >= threshold, f"Throughput is {throughput:.2f} logs/sec, which is below the required threshold of {threshold} logs/sec."