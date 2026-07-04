# test_final_state.py
import os
import re
import json
import configparser
import subprocess

def test_metrics_fstab():
    fstab_path = "/home/user/metrics_fstab"
    assert os.path.exists(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    # Check for the correct fstab line
    pattern = r"^/dev/loop99\s+/home/user/metrics_data\s+ext4\s+ro,user,noauto\s+0\s+0$"
    match = False
    for line in content.splitlines():
        if re.match(pattern, line.strip()):
            match = True
            break

    assert match, f"No line in {fstab_path} matches the required fstab format."

def test_metrics_data_directory_and_acls():
    dir_path = "/home/user/metrics_data"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    # Check ACLs using getfacl
    result = subprocess.run(["getfacl", dir_path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."

    output = result.stdout
    assert re.search(r"^user:2048:r-x$", output, re.MULTILINE), f"ACL for UID 2048 (r-x) not found on {dir_path}."
    assert re.search(r"^default:user:2048:r-x$", output, re.MULTILINE), f"Default ACL for UID 2048 (r-x) not found on {dir_path}."

def test_dash_config_ini():
    ini_path = "/home/user/dash_config.ini"
    assert os.path.exists(ini_path), f"File {ini_path} does not exist."

    config = configparser.ConfigParser()
    config.read(ini_path)

    assert "Dashboard" in config, "Section [Dashboard] missing in dash_config.ini."
    assert config["Dashboard"].get("theme") == "dark", "Theme is not 'dark'."
    assert config["Dashboard"].get("refresh_rate") == "15", "Refresh rate is not '15'."

    assert "Metrics" in config, "Section [Metrics] missing in dash_config.ini."
    assert config["Metrics"].get("source") == "/home/user/metrics_data", "Source is incorrect in [Metrics]."

def test_build_dash_script_exists():
    script_path = "/home/user/build_dash.py"
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."

def test_dashboard_json():
    json_path = "/home/user/dashboard.json"
    assert os.path.exists(json_path), f"JSON file {json_path} does not exist. Did the script run?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    expected_data = {
        "config": {
            "theme": "dark",
            "refresh": 15
        },
        "status": "tuned",
        "data_source": "/home/user/metrics_data"
    }

    assert data == expected_data, f"JSON content in {json_path} does not match expected output."
    assert isinstance(data.get("config", {}).get("refresh"), int), "Refresh value in JSON must be an integer."