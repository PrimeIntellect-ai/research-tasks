# test_final_state.py

import os
import pytest

def test_bin_server_exists_and_executable():
    bin_path = "/home/user/project/bin/server"
    assert os.path.isfile(bin_path), f"Expected binary at {bin_path} does not exist. Did 'make build' run successfully?"
    assert os.access(bin_path, os.X_OK), f"The file at {bin_path} is not executable."

def test_report_txt_contains_pass():
    report_path = "/home/user/test_report.txt"
    assert os.path.isfile(report_path), f"Test report at {report_path} does not exist. Did you pipe 'make test' output to it?"

    with open(report_path, "r") as f:
        content = f.read()

    assert "PASS" in content, f"The test report {report_path} does not contain 'PASS'. The Go tests might have failed."

def test_server_go_exists_and_uses_concurrency():
    server_go_path = "/home/user/project/go/server.go"
    assert os.path.isfile(server_go_path), f"Go source file at {server_go_path} does not exist."

    with open(server_go_path, "r") as f:
        content = f.read()

    # Check for usage of goroutines and channels
    has_go = "go " in content or "go\t" in content or "go\n" in content
    has_chan = "chan " in content or "chan\t" in content or "chan<-" in content or "<-chan" in content

    assert has_go, f"The file {server_go_path} does not appear to use goroutines ('go' keyword missing)."
    assert has_chan, f"The file {server_go_path} does not appear to use channels ('chan' keyword missing)."

def test_rules_json_exists():
    rules_json_path = "/home/user/project/rules.json"
    assert os.path.isfile(rules_json_path), f"rules.json at {rules_json_path} does not exist. Did 'make rules' run successfully?"