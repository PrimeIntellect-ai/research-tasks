# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import ssl
import time
import pytest

def test_deploy_script_exists():
    """Verify that the deploy script exists."""
    script_path = '/home/user/deploy.sh'
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."

def test_symlink_and_release_directory():
    """Verify the current symlink and release directory structure."""
    current_link = '/home/user/planner_app/current'
    assert os.path.islink(current_link), f"{current_link} is not a symlink."

    target_dir = os.readlink(current_link)
    assert os.path.isdir(current_link), f"Symlink {current_link} does not point to a valid directory."

    # Check that it points to a release directory
    assert 'releases' in target_dir or target_dir.startswith('/home/user/planner_app/releases/'), \
        f"Symlink target {target_dir} does not seem to be in the releases directory."

def test_tls_certificates_exist():
    """Verify that the TLS certificates were generated."""
    cert_path = '/home/user/planner_app/shared/certs/cert.pem'
    key_path = '/home/user/planner_app/shared/certs/key.pem'

    assert os.path.isfile(cert_path), f"TLS certificate missing at {cert_path}"
    assert os.path.isfile(key_path), f"TLS private key missing at {key_path}"

def test_analyzer_binary_and_report_json():
    """Verify the analyzer binary and the generated report.json in the current directory."""
    current_dir = '/home/user/planner_app/current'
    analyzer_path = os.path.join(current_dir, 'analyzer')
    report_path = os.path.join(current_dir, 'report.json')

    assert os.path.isfile(analyzer_path), f"Analyzer binary missing at {analyzer_path}"
    assert os.access(analyzer_path, os.X_OK), f"Analyzer binary at {analyzer_path} is not executable"

    assert os.path.isfile(report_path), f"report.json missing at {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert 'avg_cpu' in data, "report.json missing 'avg_cpu' key"
    assert 'avg_mem' in data, "report.json missing 'avg_mem' key"

    # Check values based on truth data
    assert round(float(data['avg_cpu']), 2) == 53.67, f"Expected avg_cpu to be 53.67, got {data['avg_cpu']}"
    assert round(float(data['avg_mem']), 2) == 1536.00, f"Expected avg_mem to be 1536.00, got {data['avg_mem']}"

def test_web_server_serving_report():
    """Verify the web server is running on port 9443 and serving report.json over TLS."""
    url = 'https://localhost:9443/report.json'

    # Create an unverified context to bypass self-signed cert checks
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ctx, timeout=2) as response:
                assert response.status == 200, f"Expected HTTP 200, got {response.status}"
                body = response.read().decode('utf-8')
                data = json.loads(body)
                assert 'avg_cpu' in data and 'avg_mem' in data, "Served JSON is missing expected keys"
                assert round(float(data['avg_cpu']), 2) == 53.67, "Served JSON avg_cpu is incorrect"
                assert round(float(data['avg_mem']), 2) == 1536.00, "Served JSON avg_mem is incorrect"
                return
        except urllib.error.URLError as e:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            pytest.fail(f"Failed to fetch {url} after {max_retries} attempts. Error: {e}")
        except json.JSONDecodeError:
            pytest.fail(f"Content served at {url} is not valid JSON.")