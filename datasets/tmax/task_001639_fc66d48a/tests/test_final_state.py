# test_final_state.py

import os
import urllib.request
import urllib.error
import socket
import pytest

def test_billing_active_csv():
    file_path = "/home/user/billing_active.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    expected_content = """1,EC2,us-east-1,ACTIVE,100.50
3,S3,us-west-2,ACTIVE,20.25
4,RDS,eu-central-1,ACTIVE,200.00
6,Lambda,us-east-1,ACTIVE,5.50
7,EC2,us-west-1,ACTIVE,49.50"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_go_files_exist():
    assert os.path.exists("/home/user/finops_monitor.go"), "/home/user/finops_monitor.go is missing."
    assert os.path.exists("/home/user/finops_monitor"), "/home/user/finops_monitor is missing."
    assert os.path.isfile("/home/user/finops_monitor"), "/home/user/finops_monitor is not a file."

def test_check_health_script_exists():
    assert os.path.exists("/home/user/check_health.sh"), "/home/user/check_health.sh is missing."

def test_final_metrics_txt():
    file_path = "/home/user/final_metrics.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    expected_content = """cost{service="EC2"} 150.00
cost{service="Lambda"} 5.50
cost{service="RDS"} 200.00
cost{service="S3"} 20.25"""

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {file_path} is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_port_9090_listening():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9090))
    sock.close()
    assert result == 0, "No process is listening on 127.0.0.1:9090 (Go application missing or not running)."

def test_port_8080_listening():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8080))
    sock.close()
    assert result == 0, "No process is listening on 127.0.0.1:8080 (socat missing or not running)."

def test_health_endpoint():
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            assert body == "OK", f"Expected body 'OK', got '{body}'"
    except Exception as e:
        pytest.fail(f"Failed to reach /health on port 8080: {e}")

def test_metrics_endpoint():
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/metrics")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            lines = sorted([line.strip() for line in body.splitlines() if line.strip()])
            expected_lines = [
                'cost{service="EC2"} 150.00',
                'cost{service="Lambda"} 5.50',
                'cost{service="RDS"} 200.00',
                'cost{service="S3"} 20.25'
            ]
            assert lines == expected_lines, f"Metrics output is incorrect. Expected: {expected_lines}, Got: {lines}"
    except Exception as e:
        pytest.fail(f"Failed to reach /metrics on port 8080: {e}")