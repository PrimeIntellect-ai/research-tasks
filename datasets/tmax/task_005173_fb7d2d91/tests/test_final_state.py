# test_final_state.py

import os
import json
import subprocess
import urllib.request
import ssl
from pathlib import Path

def test_health_output_file():
    """Verify the curl output saved by the user."""
    output_file = Path("/home/user/health_output.json")
    assert output_file.is_file(), f"Output file not found at {output_file}"

    content = output_file.read_text().strip()
    try:
        data = json.loads(content)
        assert data.get("status") == "healthy", "JSON output does not contain 'status': 'healthy'"
    except json.JSONDecodeError:
        assert '{"status": "healthy"}' in content.replace(" ", ""), "Output file does not contain valid expected JSON."

def test_systemd_service_active():
    """Verify that the health-server.service is active."""
    env = os.environ.copy()
    if "XDG_RUNTIME_DIR" not in env:
        env["XDG_RUNTIME_DIR"] = "/run/user/1000"

    result = subprocess.run(
        ["systemctl", "--user", "is-active", "health-server.service"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.stdout.strip() == "active", "health-server.service is not active"

def test_systemd_service_configuration():
    """Verify that the systemd service file contains archivemount and fusermount."""
    service_file = Path("/home/user/.config/systemd/user/health-server.service")
    assert service_file.is_file(), f"Service file not found at {service_file}"

    content = service_file.read_text()
    assert "archivemount" in content, "Service file does not use archivemount to mount the certificates."
    assert "fusermount" in content and "-u" in content, "Service file does not use fusermount -u to unmount the certificates."

def test_endpoint_is_reachable():
    """Verify the endpoint returns the expected JSON independently."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/health")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8').strip()
            try:
                data = json.loads(body)
                assert data.get("status") == "healthy", "Endpoint did not return {'status': 'healthy'}"
            except json.JSONDecodeError:
                assert '{"status": "healthy"}' in body.replace(" ", ""), "Endpoint did not return expected JSON."
    except Exception as e:
        assert False, f"Failed to connect to the health endpoint: {e}"