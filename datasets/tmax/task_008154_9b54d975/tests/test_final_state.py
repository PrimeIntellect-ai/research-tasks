# test_final_state.py

import os
import json
import pytest
import subprocess
import re

def get_max_glibc(filepath):
    try:
        output = subprocess.check_output(["readelf", "-V", filepath], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return "0.0"

    versions = []
    for line in output.splitlines():
        m = re.search(r'Name:\s*GLIBC_([0-9\.]+)', line)
        if m:
            versions.append(m.group(1))

    if not versions:
        return "0.0"

    def parse_ver(v):
        return tuple(int(x) for x in v.split('.'))

    return sorted(versions, key=parse_ver)[-1]

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_json_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert isinstance(data, dict), "Report JSON must be an object/dictionary."

def test_ws_received_json_exists_and_matches():
    report_path = "/home/user/report.json"
    ws_path = "/home/user/ws_received.json"

    assert os.path.isfile(ws_path), f"WebSocket received file {ws_path} is missing. Did the script send the payload?"

    with open(report_path, "r") as f:
        report_data = json.load(f)

    with open(ws_path, "r") as f:
        try:
            ws_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {ws_path} does not contain valid JSON.")

    assert report_data == ws_data, "The JSON payload received by the WebSocket server does not match the report.json file."

def test_report_json_content():
    report_path = "/home/user/report.json"
    with open(report_path, "r") as f:
        data = json.load(f)

    expected_deps = {
        "server": ["libalpha.so", "libbeta.so"],
        "libalpha.so": ["libgamma.so"],
        "libbeta.so": [],
        "libgamma.so": []
    }

    file_paths = {
        "server": "/home/user/artifact/bin/server",
        "libalpha.so": "/home/user/artifact/lib/libalpha.so",
        "libbeta.so": "/home/user/artifact/lib/libbeta.so",
        "libgamma.so": "/home/user/artifact/lib/libgamma.so"
    }

    for key, expected_dep_list in expected_deps.items():
        assert key in data, f"Missing key '{key}' in report JSON."
        assert "dependencies" in data[key], f"Missing 'dependencies' for '{key}'."
        assert "max_glibc" in data[key], f"Missing 'max_glibc' for '{key}'."

        actual_deps = data[key]["dependencies"]
        assert sorted(actual_deps) == sorted(expected_dep_list), f"Dependencies for '{key}' are incorrect. Expected {expected_dep_list}, got {actual_deps}."

        expected_glibc = get_max_glibc(file_paths[key])
        actual_glibc = data[key]["max_glibc"]
        # If the file didn't have GLIBC versioning, the expected might be "0.0", but check if it matches
        if expected_glibc != "0.0":
            assert actual_glibc == expected_glibc, f"max_glibc for '{key}' is incorrect. Expected {expected_glibc}, got {actual_glibc}."