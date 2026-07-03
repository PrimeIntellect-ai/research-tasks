# test_final_state.py
import os
import json
import stat
import pytest

def test_extract_and_clean_script():
    script_path = "/home/user/extract_and_clean.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_extracted_and_cleaned_servers_conf():
    alpha_conf = "/home/user/extracted/app_alpha/servers.conf"
    beta_conf = "/home/user/extracted/app_beta/servers.conf"

    assert os.path.isfile(alpha_conf), f"Cleaned file {alpha_conf} does not exist."
    assert os.path.isfile(beta_conf), f"Cleaned file {beta_conf} does not exist."

    with open(alpha_conf, "r") as f:
        alpha_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    expected_alpha = ["192.168.1.10", "192.168.1.11", "10.0.0.5"]
    assert alpha_lines == expected_alpha, f"Expected {alpha_conf} to have {expected_alpha}, got {alpha_lines}."

    with open(beta_conf, "r") as f:
        beta_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    expected_beta = ["172.16.0.4", "172.16.0.5"]
    assert beta_lines == expected_beta, f"Expected {beta_conf} to have {expected_beta}, got {beta_lines}."

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_data = {
        "admin_commits": 3,
        "apps": {
            "app_alpha": {
                "servers": ["192.168.1.10", "192.168.1.11", "10.0.0.5"],
                "config_keys": {
                    "db_port": 5432,
                    "max_conn": 100
                }
            },
            "app_beta": {
                "servers": ["172.16.0.4", "172.16.0.5"],
                "config_keys": {
                    "cache_size": 2048
                }
            }
        }
    }

    assert report_data == expected_data, f"Report JSON does not match expected output.\nExpected: {expected_data}\nGot: {report_data}"