# test_final_state.py
import os
import json
import subprocess
import requests

def test_config_json_exists():
    config_path = "/home/user/config.json"
    assert os.path.isfile(config_path), f"{config_path} does not exist"
    with open(config_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{config_path} does not contain valid JSON"
    assert "DASH-99" in str(data), "config.json does not seem to contain DASH-99"

def test_systemd_service_file():
    service_path = os.path.expanduser("~/.config/systemd/user/video-metrics.service")
    assert os.path.isfile(service_path), f"Systemd service file {service_path} does not exist"

    with open(service_path, "r") as f:
        content = f.read()

    assert "After=network.target" in content, "Service file does not contain 'After=network.target'"

def test_systemd_service_active():
    try:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", "video-metrics.service"],
            capture_output=True,
            text=True,
            check=True
        )
        assert result.stdout.strip() == "active", "video-metrics.service is not active"
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to check service status, output: {e.stdout}, err: {e.stderr}"

def test_http_metrics_endpoint():
    url = "http://127.0.0.1:9090/metrics"
    headers = {"Authorization": "Bearer DASH-99"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to {url}: {e}"

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert data.get("dashboard_id") == "DASH-99", f"Expected dashboard_id 'DASH-99', got {data.get('dashboard_id')}"
    assert data.get("red_alerts_count") == 12, f"Expected red_alerts_count 12, got {data.get('red_alerts_count')}"