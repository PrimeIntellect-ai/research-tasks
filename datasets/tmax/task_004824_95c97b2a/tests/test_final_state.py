# test_final_state.py
import os
import difflib
import pytest
import urllib.request
import urllib.error

def test_nginx_config_restored():
    """Verify Nginx configuration routes to the Flask app."""
    config_path = "/app/services/nginx.conf"
    assert os.path.isfile(config_path), f"{config_path} is missing"
    with open(config_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://localhost:5000;" in content, "Nginx config not correctly restored to proxy to port 5000"

def test_env_file_restored():
    """Verify Flask environment variables are configured for Redis."""
    env_path = "/app/services/.env"
    assert os.path.isfile(env_path), f"{env_path} is missing"
    with open(env_path, "r") as f:
        content = f.read()
    assert "REDIS_HOST=localhost" in content, "REDIS_HOST not set to localhost in .env"
    assert "REDIS_PORT=6379" in content, "REDIS_PORT not set to 6379 in .env"

def test_audit_report_exists_and_correct():
    """Verify the audit report identifies the misconfigured SUID binary."""
    report_path = "/home/user/audit_report.txt"
    assert os.path.isfile(report_path), f"{report_path} is missing"
    with open(report_path, "r") as f:
        content = f.read()
    assert "backup_util" in content, "Audit report does not identify the correct SUID binary (backup_util)"

def test_recover_script_exists():
    """Verify the recovery script was created."""
    assert os.path.isfile("/home/user/recover.py"), "/home/user/recover.py is missing"

def test_recovered_evidence_metric():
    """Verify the recovered evidence meets the similarity threshold."""
    recovered_path = "/home/user/recovered_evidence.txt"
    reference_path = "/app/.secret_reference.txt"

    assert os.path.isfile(recovered_path), f"{recovered_path} is missing"
    assert os.path.isfile(reference_path), f"{reference_path} is missing"

    with open(recovered_path, "r") as f:
        recovered = f.read()
    with open(reference_path, "r") as f:
        reference = f.read()

    ratio = difflib.SequenceMatcher(None, recovered, reference).ratio()
    assert ratio >= 0.98, f"Similarity ratio {ratio} is below the 0.98 threshold. The recovered text does not sufficiently match the reference."

def test_health_endpoint():
    """Verify the end-to-end flow is working by hitting the health endpoint."""
    try:
        req = urllib.request.Request("http://localhost:8080/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            assert status == 200, f"Health endpoint returned status {status}"
            assert '"status":' in body and '"ok"' in body, f"Unexpected health response: {body}"
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to health endpoint: {e}. Ensure the services are running.")