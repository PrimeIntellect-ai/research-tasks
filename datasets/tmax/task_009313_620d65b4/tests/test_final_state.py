# test_final_state.py

import os
import tarfile
import json
import re
import pytest

def test_backup_archive_exists_and_valid():
    backup_path = "/home/user/backups/dashboard_active_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive missing at {backup_path}"

    # Check contents of the tar file
    with tarfile.open(backup_path, "r:gz") as tar:
        members = tar.getnames()

        # Look for cpu.json and mem.json in the archive
        cpu_member = next((m for m in members if m.endswith("cpu.json")), None)
        mem_member = next((m for m in members if m.endswith("mem.json")), None)

        assert cpu_member is not None, "cpu.json missing from backup archive"
        assert mem_member is not None, "mem.json missing from backup archive"

        # Read contents
        cpu_f = tar.extractfile(cpu_member)
        mem_f = tar.extractfile(mem_member)

        assert cpu_f is not None, "Could not extract cpu.json from archive"
        assert mem_f is not None, "Could not extract mem.json from archive"

        cpu_content = cpu_f.read().decode('utf-8').strip()
        mem_content = mem_f.read().decode('utf-8').strip()

        assert "CPU" in cpu_content and "CPU V2" not in cpu_content, "Backup cpu.json does not have original content"
        assert "Memory" in mem_content and "Memory V2" not in mem_content, "Backup mem.json does not have original content"

def test_active_dashboards_updated():
    cpu_path = "/home/user/dashboards/active/cpu.json"
    mem_path = "/home/user/dashboards/active/mem.json"

    assert os.path.isfile(cpu_path), f"Deployed file {cpu_path} is missing"
    assert os.path.isfile(mem_path), f"Deployed file {mem_path} is missing"

    with open(cpu_path, "r") as f:
        cpu_data = json.load(f)
        assert cpu_data.get("title") == "CPU V2", f"cpu.json was not updated correctly: {cpu_data}"

    with open(mem_path, "r") as f:
        mem_data = json.load(f)
        assert mem_data.get("title") == "Memory V2", f"mem.json was not updated correctly: {mem_data}"

def test_invalid_dashboard_not_deployed():
    network_path = "/home/user/dashboards/active/network.json"
    assert not os.path.exists(network_path), f"Invalid JSON file {network_path} should not have been deployed"

def test_error_log_contents():
    log_path = "/home/user/logs/deploy_errors.log"
    assert os.path.isfile(log_path), f"Error log missing at {log_path}"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    expected_line = "ERROR: network.json is invalid JSON."
    assert expected_line in log_content, f"Error log does not contain the expected error message. Found: {log_content}"

def test_forward_dashboard_script():
    script_path = "/home/user/scripts/forward_dashboard.sh"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    with open(script_path, "r") as f:
        content = f.read().lower()

    assert "socat" in content, "Script does not use socat"
    assert "8080" in content, "Script does not reference port 8080"
    assert "9090" in content, "Script does not reference port 9090"

    # Check for correct socat forwarding syntax
    # e.g. socat TCP-LISTEN:8080,fork TCP:127.0.0.1:9090
    assert re.search(r'tcp(-listen|l)?:8080', content), "Script does not correctly listen on port 8080"
    assert re.search(r'tcp:127\.0\.0\.1:9090', content), "Script does not correctly forward to 127.0.0.1:9090"
    assert "&" in content or "fork" in content, "Script does not run in background or use fork"