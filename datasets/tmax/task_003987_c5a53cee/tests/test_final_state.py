# test_final_state.py

import os
import csv
import math
import subprocess
import pytest

def get_expected_min_cost(traffic_file):
    expected_cost = 0.0
    with open(traffic_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rate = float(row['request_rate'])
            # Latency = (rate * 500) / (A^2) <= 200
            # A^2 >= (rate * 500) / 200 = rate * 2.5
            min_a2 = rate * 2.5
            A = math.ceil(math.sqrt(min_a2))
            if A < 1:
                A = 1
            elif A > 100:
                A = 100
            cost = A * 2.5 + rate * 0.01
            expected_cost += cost
    return expected_cost

def test_optimal_allocations_cost():
    allocations_file = '/home/user/optimal_allocations.csv'
    traffic_file = '/home/user/traffic.csv'

    assert os.path.isfile(allocations_file), f"File {allocations_file} does not exist."

    expected_cost = get_expected_min_cost(traffic_file)
    threshold_cost = expected_cost + 2.0  # Allow some small margin as per prompt (618 -> 620)

    total_cost = 0.0
    with open(allocations_file, 'r') as f:
        reader = csv.DictReader(f)
        assert 'cost' in reader.fieldnames, "The 'cost' column is missing from optimal_allocations.csv."
        for row in reader:
            total_cost += float(row['cost'])

    assert total_cost > 0, f"Total cost is {total_cost}, which is invalid."
    assert total_cost <= threshold_cost, f"Total cost {total_cost} exceeds the threshold of {threshold_cost}. Expected around {expected_cost}."

def test_nginx_config_generated():
    nginx_conf = '/home/user/optimized_nginx.conf'
    assert os.path.isfile(nginx_conf), f"Nginx config {nginx_conf} does not exist."

    with open(nginx_conf, 'r') as f:
        content = f.read()

    assert 'listen 8080' in content or 'listen  8080' in content, "Nginx config does not listen on port 8080."
    assert 'proxy_pass http://127.0.0.1:9000' in content, "Nginx config does not proxy to http://127.0.0.1:9000."
    assert 'log_format finops' in content or 'log_format  finops' in content, "Nginx config does not define a 'finops' log format."
    assert '/home/user/logs/access.log' in content, "Nginx config does not log to /home/user/logs/access.log."

    # Check for endpoints
    endpoints = ['/api/v1/users', '/api/v1/products', '/api/v1/orders', '/api/v2/catalog']
    for ep in endpoints:
        assert ep in content, f"Nginx config is missing a location block for {ep}."

def test_logrotate_config():
    logrotate_conf = '/home/user/logrotate.conf'
    assert os.path.isfile(logrotate_conf), f"Logrotate config {logrotate_conf} does not exist."

    with open(logrotate_conf, 'r') as f:
        content = f.read()

    assert 'daily' in content, "logrotate config does not specify 'daily' rotation."
    assert 'rotate 7' in content, "logrotate config does not specify keeping 7 days of logs ('rotate 7')."
    assert 'compress' in content, "logrotate config does not specify 'compress'."

def test_nginx_is_running():
    # Check if nginx is listening on port 8080 or process is running
    try:
        output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
        assert 'nginx' in output, "Nginx process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to check running processes.")