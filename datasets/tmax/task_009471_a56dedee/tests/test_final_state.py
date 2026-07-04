# test_final_state.py
import os
import re
import pytest

def test_auth_conf_updated():
    auth_file = "/home/user/.config/reporter/auth.conf"
    assert os.path.isfile(auth_file), f"Auth file missing: {auth_file}"

    with open(auth_file, "r") as f:
        content = f.read()

    server_script = "/home/user/reporting_service.py"
    assert os.path.isfile(server_script), f"Reporting service script missing: {server_script}"

    with open(server_script, "r") as f:
        server_content = f.read()

    match = re.search(r'EXPECTED_TOKEN\s*=\s*["\']([^"\']+)["\']', server_content)
    assert match is not None, "Could not find EXPECTED_TOKEN in reporting_service.py"
    expected_token = match.group(1)

    assert expected_token in content, f"auth.conf does not contain the correct token. Expected to find: {expected_token}"

def test_csv_content():
    csv_file = "/home/user/capacity_report.csv"
    assert os.path.isfile(csv_file), f"CSV report missing: {csv_file}"

    base_dir = "/home/user/mock_containers"
    expected_sizes = {}
    if os.path.isdir(base_dir):
        for container in os.listdir(base_dir):
            data_dir = os.path.join(base_dir, container, "data")
            total_size = 0
            if os.path.isdir(data_dir):
                for root, _, files in os.walk(data_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            total_size += os.path.getsize(file_path)
            expected_sizes[container] = total_size

    expected_csv_lines = [f"{c},{expected_sizes[c]}" for c in sorted(expected_sizes.keys())]

    with open(csv_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_csv_lines, f"CSV content mismatch. Expected: {expected_csv_lines}, Got: {actual_lines}"

def test_server_success_flag():
    flag_file = "/home/user/server_success.flag"
    assert os.path.isfile(flag_file), "server_success.flag was not created. The POST request to the reporting service likely failed or was rejected."

    with open(flag_file, "r") as f:
        content = f.read().strip()

    assert content == "SUCCESS", f"server_success.flag contains '{content}', expected 'SUCCESS'"

def test_scripts_exist():
    analyzer_cpp = "/home/user/analyzer.cpp"
    assert os.path.isfile(analyzer_cpp), f"C++ analyzer source missing: {analyzer_cpp}"

    submit_script = "/home/user/submit_metrics.sh"
    assert os.path.isfile(submit_script), f"Automation script missing: {submit_script}"
    assert os.access(submit_script, os.X_OK), f"Automation script is not executable: {submit_script}"