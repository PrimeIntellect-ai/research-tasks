# test_final_state.py

import os
import json
import ast
import pytest

REPORT_PATH = '/home/user/scan_report.json'
SCRIPT_PATH = '/home/user/scan_configs.py'

def test_report_exists():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    assert os.path.isfile(REPORT_PATH), f"Report path {REPORT_PATH} is not a file."

def test_report_contents():
    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {REPORT_PATH} is not valid JSON.")

    assert "safe_packs" in report, "Key 'safe_packs' missing from report."
    assert "malicious_packs" in report, "Key 'malicious_packs' missing from report."

    expected_safe = [
        "/home/user/incoming/valid.cfgpack"
    ]
    expected_malicious = [
        "/home/user/incoming/evil.cfgpack",
        "/home/user/incoming/subdir/absolute.cfgpack"
    ]

    assert report["safe_packs"] == expected_safe, \
        f"Expected safe_packs to be {expected_safe}, but got {report['safe_packs']}"

    assert report["malicious_packs"] == expected_malicious, \
        f"Expected malicious_packs to be {expected_malicious}, but got {report['malicious_packs']}"

def test_script_exists_and_uses_atomic_write():
    assert os.path.exists(SCRIPT_PATH), f"Script file {SCRIPT_PATH} does not exist."

    with open(SCRIPT_PATH, 'r') as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError:
        pytest.fail(f"Script {SCRIPT_PATH} contains a syntax error.")

    # Check for os.replace, os.rename, or shutil.move
    found_atomic_write = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                func_name = node.func.attr
                if isinstance(node.func.value, ast.Name):
                    module_name = node.func.value.id
                    if (module_name == 'os' and func_name in ('replace', 'rename')) or \
                       (module_name == 'shutil' and func_name == 'move'):
                        found_atomic_write = True
                        break

    assert found_atomic_write, \
        "Script does not appear to use os.replace, os.rename, or shutil.move for atomic writing."