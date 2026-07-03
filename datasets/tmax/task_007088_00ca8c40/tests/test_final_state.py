# test_final_state.py

import os
import json
import pytest

def get_dir_size_bytes(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def test_scripts_exist():
    py_script = "/home/user/scripts/update_routing.py"
    sh_script = "/home/user/scripts/run_checks.sh"

    assert os.path.isfile(py_script), f"Python script missing: {py_script}"
    assert os.path.isfile(sh_script), f"Bash script missing: {sh_script}"
    assert os.access(sh_script, os.X_OK), f"Bash script is not executable: {sh_script}"

def test_config_updated_in_place():
    config_path = "/home/user/config/router.json"
    assert os.path.isfile(config_path), f"Config file missing: {config_path}"

    with open(config_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {config_path} is not valid JSON")

    assert "global_settings" in data, "Missing 'global_settings' in config"
    assert data["global_settings"].get("timeout") == 30, "Incorrect global_settings.timeout"
    assert data["global_settings"].get("retries") == 3, "Incorrect global_settings.retries"

    assert "nodes" in data, "Missing 'nodes' in config"

    for node_name, node_info in data["nodes"].items():
        node_path = node_info.get("path")
        assert node_path, f"Missing path for node {node_name}"
        assert os.path.isdir(node_path), f"Node path does not exist: {node_path}"

        size_bytes = get_dir_size_bytes(node_path)
        # 40 Megabytes = 40960 Kilobytes = 41943040 bytes
        # Some interpretations might use 40 * 1000 * 1000, but 40 * 1024 * 1024 is standard for MB/MiB in this context.
        # The test files are 45MB, 15MB, 50MB, so the difference is large enough to not be affected by MB vs MiB.
        expected_status = "offline" if size_bytes > 40 * 1024 * 1024 else "online"
        actual_status = node_info.get("status")

        assert actual_status == expected_status, \
            f"Node {node_name} status is '{actual_status}', expected '{expected_status}' based on size {size_bytes} bytes"

def test_final_log_exists_and_correct():
    log_path = "/home/user/logs/final_router.json"
    assert os.path.isfile(log_path), f"Final log file missing: {log_path}. Did the bash script run and copy the file?"

    with open(log_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {log_path} is not valid JSON")

    # Verify specific nodes according to the truth data
    nodes = data.get("nodes", {})
    assert nodes.get("node1", {}).get("status") == "offline", "node1 should be offline"
    assert nodes.get("node2", {}).get("status") == "online", "node2 should be online"
    assert nodes.get("node3", {}).get("status") == "offline", "node3 should be offline"

    global_settings = data.get("global_settings", {})
    assert global_settings.get("timeout") == 30, "global_settings.timeout should be preserved as 30"
    assert global_settings.get("retries") == 3, "global_settings.retries should be preserved as 3"