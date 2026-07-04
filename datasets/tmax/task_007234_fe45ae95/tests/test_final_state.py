# test_final_state.py

import os
import json
import pytest
import datetime
import locale

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo

def test_auth_endpoint_extracted():
    endpoint_path = "/home/user/config/auth_endpoint.txt"
    assert os.path.isfile(endpoint_path), f"File {endpoint_path} does not exist."

    with open(endpoint_path, "r") as f:
        content = f.read().strip()

    assert content == "192.168.100.45:8081", f"Expected '192.168.100.45:8081' in {endpoint_path}, but got '{content}'."

def test_services_json_modified():
    json_path = "/home/user/config/services.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    api_gateway_deps = data.get("services", {}).get("api-gateway", {}).get("depends_on", [])
    assert "auth-service" in api_gateway_deps, "The 'auth-service' was not added to the 'depends_on' array for 'api-gateway'."

def test_gateway_startup_log():
    log_path = "/home/user/logs/gateway_startup.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did the Python script run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    # Recompute the expected localized time string
    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    except locale.Error:
        pytest.fail("Locale de_DE.UTF-8 is not available on the system.")

    dt = datetime.datetime.fromtimestamp(1716388800, tz=zoneinfo.ZoneInfo("Europe/Berlin"))
    expected_time_str = dt.strftime('%A, %d. %B %Y %H:%M:%S')

    expected_log_entry = f"Gateway ready. Auth upstream: 192.168.100.45:8081. Local startup time: {expected_time_str}"

    assert content == expected_log_entry, f"Expected log entry:\n'{expected_log_entry}'\nBut got:\n'{content}'"