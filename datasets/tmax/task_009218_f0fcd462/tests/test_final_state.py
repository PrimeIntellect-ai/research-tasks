# test_final_state.py

import os
import json
import csv
import pytest

def test_no_path_traversal():
    assert not os.path.exists('/home/user/evil.sh'), "Path traversal vulnerability exploited: /home/user/evil.sh was extracted"

def test_no_bad_symlink():
    badlink_path = '/home/user/configs/badlink'
    if os.path.islink(badlink_path):
        target = os.readlink(badlink_path)
        assert target != '/etc/passwd', "Symlink vulnerability exploited: badlink points to /etc/passwd"

        abs_target = os.path.abspath(os.path.join('/home/user/configs', target))
        assert abs_target.startswith('/home/user/configs'), "Symlink points outside target directory"

def test_configs_state():
    app1_path = '/home/user/configs/app1.json'
    app2_path = '/home/user/configs/app2.json'
    app3_path = '/home/user/configs/app3.json'

    assert os.path.isfile(app1_path), f"{app1_path} is missing"
    with open(app1_path, 'r') as f:
        data = json.load(f)
        assert data.get("version") == "1.1", f"app1.json version should be updated to 1.1, got {data.get('version')}"

    assert os.path.isfile(app2_path), f"{app2_path} is missing"
    with open(app2_path, 'r') as f:
        data = json.load(f)
        assert data.get("version") == "1.2", f"app2.json version should remain 1.2, got {data.get('version')}"

    assert os.path.isfile(app3_path), f"{app3_path} is missing"
    with open(app3_path, 'r') as f:
        data = json.load(f)
        assert data.get("version") == "2.0", f"app3.json version should be 2.0, got {data.get('version')}"

def test_csv_summary():
    csv_path = '/home/user/config_summary.csv'
    assert os.path.isfile(csv_path), f"{csv_path} is missing"

    expected_rows = [
        ['filename', 'version'],
        ['app1.json', '1.1'],
        ['app2.json', '1.2'],
        ['app3.json', '2.0']
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows == expected_rows, f"CSV content does not match expected. Got: {rows}"