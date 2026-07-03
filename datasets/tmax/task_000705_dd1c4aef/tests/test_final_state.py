# test_final_state.py
import json
import os
import subprocess
import ast

def test_config_recovered():
    config_path = "/home/user/async_service/config.json"
    assert os.path.isfile(config_path), "config.json was not recovered to /home/user/async_service/config.json"
    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, "config.json is not valid JSON"
    assert "SECRET_KEY" in config, "config.json does not contain SECRET_KEY"
    assert config["SECRET_KEY"] == "sk_prod_99x2b_a1z", "SECRET_KEY value is incorrect in config.json"

def test_resolution_report_exists_and_valid():
    report_path = "/home/user/resolution_report.json"
    assert os.path.isfile(report_path), "resolution_report.json is missing"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "resolution_report.json is not valid JSON"

    assert "secret_key" in report, "resolution_report.json missing 'secret_key'"
    assert report["secret_key"] == "sk_prod_99x2b_a1z", "Incorrect secret_key in resolution_report.json"

    assert "fixed_files" in report, "resolution_report.json missing 'fixed_files'"
    assert "server.py" in report["fixed_files"], "server.py not listed in fixed_files"

    assert "culprit_commit" in report, "resolution_report.json missing 'culprit_commit'"

    # Derive the expected culprit commit from git history
    repo_dir = "/home/user/async_service"
    try:
        output = subprocess.check_output(
            ["git", "log", "--grep=Feature: add heavy background processing per request", "--format=%H"],
            cwd=repo_dir,
            text=True
        ).strip()
        expected_commit = output.splitlines()[0] if output else ""
    except Exception:
        expected_commit = ""

    assert expected_commit != "", "Could not find culprit commit in git history"
    assert report["culprit_commit"] == expected_commit, f"Incorrect culprit_commit in resolution_report.json. Expected {expected_commit}"

def test_server_py_fixed_and_assert_added():
    server_path = "/home/user/async_service/server.py"
    assert os.path.isfile(server_path), "server.py is missing"

    with open(server_path, 'r') as f:
        content = f.read()

    assert "cancel()" in content, "server.py does not appear to call cancel() on the background task"
    assert "assert" in content, "server.py does not contain an assert statement to validate the fix"

    # Parse AST to ensure there's an assert statement
    try:
        tree = ast.parse(content)
    except SyntaxError:
        assert False, "server.py has invalid Python syntax"

    has_assert = any(isinstance(node, ast.Assert) for node in ast.walk(tree))
    assert has_assert, "No assert statement found in server.py AST"