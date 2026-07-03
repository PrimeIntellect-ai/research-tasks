# test_final_state.py

import os
import json
import re
import subprocess
import pytest

def get_entry_point(binary_path):
    try:
        output = subprocess.check_output(['readelf', '-h', binary_path], universal_newlines=True)
        for line in output.splitlines():
            if "Entry point address:" in line:
                # Example line: "  Entry point address:               0x401000"
                parts = line.strip().split()
                return parts[-1].lower()
    except Exception:
        pass
    return None

def test_audit_report_json():
    report_path = "/home/user/audit_report.json"
    assert os.path.exists(report_path), f"Missing required file: {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not a valid JSON file")

    assert "entry_point" in data, "Missing 'entry_point' in JSON report"
    assert "policy" in data, "Missing 'policy' in JSON report"
    assert "cert_cn" in data, "Missing 'cert_cn' in JSON report"

    expected_entry_point = get_entry_point("/home/user/app_binary")
    assert expected_entry_point is not None, "Could not determine entry point of app_binary"

    # Allow matching with or without leading zeros after 0x if necessary, but exact match is preferred
    # The task says "formatted as a lowercase hex string with the 0x prefix"
    actual_ep = data["entry_point"].lower()
    assert actual_ep == expected_entry_point or actual_ep == hex(int(expected_entry_point, 16)), \
        f"Expected entry_point to be {expected_entry_point}, got {data['entry_point']}"

    assert data["policy"] == "PORT=8443", f"Expected policy to be 'PORT=8443', got {data['policy']}"
    assert data["cert_cn"] == "SecureCorpApp", f"Expected cert_cn to be 'SecureCorpApp', got {data['cert_cn']}"

def test_fw_config_sh():
    script_path = "/home/user/fw_config.sh"
    assert os.path.exists(script_path), f"Missing required file: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.strip().startswith('#')]
    assert len(lines) >= 2, "fw_config.sh must contain at least two iptables commands"

    # Regex for ACCEPT rule
    # iptables -A INPUT -p tcp --dport 8443 -s 192.168.1.100 -j ACCEPT
    accept_pattern = re.compile(r'iptables\s+.*-p\s+tcp\s+.*--dport\s+8443\s+.*-s\s+192\.168\.1\.100\s+.*-j\s+ACCEPT')

    # Regex for DROP rule
    # iptables -A INPUT -p tcp --dport 8443 -j DROP
    drop_pattern = re.compile(r'iptables\s+.*-p\s+tcp\s+.*--dport\s+8443\s+.*-j\s+DROP')

    accept_found = any(accept_pattern.search(line) for line in lines)
    drop_found = any(drop_pattern.search(line) for line in lines)

    assert accept_found, "fw_config.sh missing correct ACCEPT rule for port 8443 and IP 192.168.1.100"
    assert drop_found, "fw_config.sh missing correct DROP rule for port 8443"

def test_rust_project_exists():
    cargo_toml = "/home/user/elf_auditor/Cargo.toml"
    assert os.path.exists(cargo_toml), f"Missing Rust project file: {cargo_toml}"