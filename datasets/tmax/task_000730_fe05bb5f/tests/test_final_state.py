# test_final_state.py

import os
import json
import re

def test_monitor_go_exists():
    """Test that the Go monitoring agent source file exists."""
    assert os.path.exists("/home/user/monitor.go"), "/home/user/monitor.go does not exist."

def test_storage_metric_json():
    """Test that storage_metric.json is generated correctly based on device_storage.txt."""
    txt_path = "/home/user/device_storage.txt"
    json_path = "/home/user/storage_metric.json"

    assert os.path.exists(txt_path), f"{txt_path} is missing, cannot verify."
    assert os.path.exists(json_path), f"{json_path} was not generated."

    with open(txt_path, "r") as f:
        content = f.read().strip()

    match = re.search(r"storage_available_kb=(\d+)", content)
    assert match is not None, f"Could not parse storage_available_kb from {txt_path}"

    kb_val = int(match.group(1))
    expected_mb = kb_val // 1024

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    assert "storage_mb" in data, f"'storage_mb' key missing in {json_path}"
    assert data["storage_mb"] == expected_mb, f"Expected storage_mb to be {expected_mb}, got {data['storage_mb']}"

def test_setup_iot_script():
    """Test that setup_iot.sh exists and contains the required commands."""
    script_path = "/home/user/setup_iot.sh"
    assert os.path.exists(script_path), f"{script_path} does not exist."

    with open(script_path, "r") as f:
        script_content = f.read()

    # Check group creation
    assert re.search(r"(groupadd|addgroup)\s+sensor-net", script_content), \
        "setup_iot.sh is missing the command to create the sensor-net group."

    # Check user creation
    assert re.search(r"(useradd|adduser).*sensor-net.*metrics-agent", script_content), \
        "setup_iot.sh is missing the command to create the metrics-agent user in the sensor-net group."

    # Check route addition
    assert re.search(r"ip\s+route\s+add\s+172\.16\.0\.0/12\s+via\s+10\.0\.0\.1\s+dev\s+eth0", script_content), \
        "setup_iot.sh is missing the correct 'ip route add' command."

    # Check SSH tunnel
    ssh_pattern = r"ssh\s+.*-f.*-N.*-L\s*8080:172\.16\.5\.5:80.*tunnel@10\.0\.0\.254"
    # The flags can be in different orders, so let's do a more robust check:
    has_ssh = "ssh " in script_content
    has_f = re.search(r"\B-f\b", script_content)
    has_N = re.search(r"\B-N\b", script_content)
    has_L = re.search(r"\B-L\s+8080:172\.16\.5\.5:80\b", script_content)
    has_target = "tunnel@10.0.0.254" in script_content

    assert has_ssh and has_f and has_N and has_L and has_target, \
        "setup_iot.sh is missing the correct SSH tunnel command with -f, -N, -L 8080:172.16.5.5:80, and tunnel@10.0.0.254."