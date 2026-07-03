# test_final_state.py

import os
import json
import hashlib
import subprocess
import pytest

def test_network_script():
    script_path = "/home/user/harden_net.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "ip route add blackhole 203.0.113.0/24" in content, "Blackhole route command missing."
    assert "ip link set dev eth0 mtu 1400" in content or "ip link set eth0 mtu 1400" in content, "MTU command missing."

def test_filesystem_setup():
    app_conf = "/home/user/secure_configs/app.conf"
    db_conf = "/home/user/secure_configs/db.conf"

    assert os.path.isfile(app_conf), f"{app_conf} missing."
    assert os.path.isfile(db_conf), f"{db_conf} missing."

    with open(app_conf, "rb") as f:
        assert f.read() == b"PORT=8080", "app.conf content is incorrect or has trailing newline."

    with open(db_conf, "rb") as f:
        assert f.read() == b"MAX_CONNS=50", "db.conf content is incorrect or has trailing newline."

def test_rust_integrity_monitor():
    cargo_toml = "/home/user/fs_monitor/Cargo.toml"
    binary = "/home/user/fs_monitor/target/release/fs_monitor"
    report = "/home/user/audit_report.json"

    assert os.path.isfile(cargo_toml), f"{cargo_toml} missing."
    assert os.path.isfile(binary), f"Compiled binary {binary} missing."
    assert os.path.isfile(report), f"Audit report {report} missing."

    with open(report, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("audit_report.json is not valid JSON.")

    assert "files" in data, "'files' key missing in JSON."
    files = data["files"]
    assert len(files) == 2, "JSON should contain exactly 2 files."

    assert files[0]["name"] == "app.conf", "First file must be app.conf (sorted alphabetically)."
    assert files[1]["name"] == "db.conf", "Second file must be db.conf."

    app_hash = hashlib.sha256(b"PORT=8080").hexdigest()
    db_hash = hashlib.sha256(b"MAX_CONNS=50").hexdigest()

    assert files[0]["hash"] == app_hash, "Hash for app.conf is incorrect."
    assert files[1]["hash"] == db_hash, "Hash for db.conf is incorrect."

def test_scheduled_task():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab.")

    lines = output.strip().split("\n")
    found = False
    for line in lines:
        if line.startswith("#"):
            continue
        if "*/15" in line and "/home/user/fs_monitor/target/release/fs_monitor" in line and "2> /home/user/fs_monitor_error.log" in line:
            if not "> /home/user/fs_monitor_error.log" in line.replace("2>", ">"):
                pass # just checking that standard output is not redirected, but standard error is
            if ">" in line and not "2>" in line:
                continue
            found = True
            break

    assert found, "Cron job not found or incorrectly configured."