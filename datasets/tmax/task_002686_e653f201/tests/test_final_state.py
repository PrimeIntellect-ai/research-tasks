# test_final_state.py

import os
import stat
import subprocess
import json

def test_directories_and_permissions():
    data_dir = "/home/user/edge_package/data"
    keys_dir = "/home/user/edge_package/keys"

    assert os.path.isdir(data_dir), f"Directory {data_dir} does not exist."
    assert os.path.isdir(keys_dir), f"Directory {keys_dir} does not exist."

    mode = stat.S_IMODE(os.stat(data_dir).st_mode)
    assert mode == 0o700, f"Permissions for {data_dir} are {oct(mode)}, expected 0o700."

def test_ssh_keys():
    priv_key = "/home/user/edge_package/keys/iot_key"
    pub_key = "/home/user/edge_package/keys/iot_key.pub"

    assert os.path.isfile(priv_key), f"Private key {priv_key} does not exist."
    assert os.path.isfile(pub_key), f"Public key {pub_key} does not exist."

    with open(priv_key, 'r') as f:
        content = f.read()
    assert "PRIVATE KEY" in content, "File does not appear to be a private key."

def test_network_setup_script():
    script = "/home/user/edge_package/network_setup.sh"
    assert os.path.isfile(script), f"Script {script} does not exist."
    assert os.access(script, os.X_OK), f"Script {script} is not executable."

    with open(script, 'r') as f:
        content = f.read()

    assert "ip link add" in content and "sensor-net" in content and "dummy" in content, "network_setup.sh missing correct 'ip link add' command."
    assert "ip addr add 192.168.100.1/24" in content and "sensor-net" in content, "network_setup.sh missing correct 'ip addr add' command."

def test_tunnel_script():
    script = "/home/user/edge_package/tunnel.sh"
    assert os.path.isfile(script), f"Script {script} does not exist."
    assert os.access(script, os.X_OK), f"Script {script} is not executable."

    with open(script, 'r') as f:
        content = f.read()

    assert "ssh " in content, "tunnel.sh missing ssh command."
    assert "-f" in content, "tunnel.sh missing -f flag."
    assert "-N" in content, "tunnel.sh missing -N flag."
    assert "-L" in content, "tunnel.sh missing -L flag."
    assert "8080" in content, "tunnel.sh missing local port 8080."
    assert "9000" in content, "tunnel.sh missing remote port 9000."
    assert "192.168.100.5" in content, "tunnel.sh missing target IP 192.168.100.5."
    assert "sensor_user" in content, "tunnel.sh missing user sensor_user."
    assert "/home/user/edge_package/keys/iot_key" in content, "tunnel.sh missing correct SSH key path."

def test_verify_data_script():
    script = "/home/user/edge_package/verify_data.py"
    assert os.path.isfile(script), f"Script {script} does not exist."
    assert os.access(script, os.X_OK), f"Script {script} is not executable."

    # Test with valid status
    test_json_1 = json.dumps({"status": "active"})
    proc = subprocess.run([script], input=test_json_1, text=True, capture_output=True)
    assert proc.returncode == 0, f"verify_data.py failed to run. Stderr: {proc.stderr}"
    assert proc.stdout.strip() == "active", f"Expected 'active', got {proc.stdout.strip()}"

    # Test with missing status
    test_json_2 = json.dumps({"data": "none"})
    proc2 = subprocess.run([script], input=test_json_2, text=True, capture_output=True)
    assert proc2.returncode == 0, f"verify_data.py failed to run. Stderr: {proc2.stderr}"
    assert proc2.stdout.strip() == "unknown", f"Expected 'unknown', got {proc2.stdout.strip()}"