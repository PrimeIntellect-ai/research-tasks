# test_final_state.py
import os
import re
import pytest

def test_files_exist():
    expected_files = [
        "/home/user/semver_filter.cpp",
        "/home/user/deploy_workers.go",
        "/home/user/ci_pipeline.sh",
        "/home/user/valid_versions.txt",
        "/home/user/deploy_log.txt"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected file {f} is missing."

def test_valid_versions_content():
    valid_versions_file = "/home/user/valid_versions.txt"
    expected_versions = {
        "2.0.0-rc1",
        "2.0.0-rc2",
        "2.0.0",
        "2.0.1",
        "3.0.0-beta"
    }

    with open(valid_versions_file, "r") as f:
        content = set(line.strip() for line in f if line.strip())

    assert content == expected_versions, f"Content of {valid_versions_file} does not match the expected valid versions."

def test_deploy_log_content():
    deploy_log_file = "/home/user/deploy_log.txt"
    expected_lines = {
        "Deployed version: 2.0.0",
        "Deployed version: 2.0.0-rc1",
        "Deployed version: 2.0.0-rc2",
        "Deployed version: 2.0.1",
        "Deployed version: 3.0.0-beta"
    }

    with open(deploy_log_file, "r") as f:
        content = sorted([line.strip() for line in f if line.strip()])

    assert len(content) == 5, f"Expected exactly 5 lines in {deploy_log_file}, but found {len(content)}."
    assert set(content) == expected_lines, f"Content of {deploy_log_file} does not match expected deployed versions."

def test_go_worker_pool_implementation():
    go_file = "/home/user/deploy_workers.go"
    with open(go_file, "r") as f:
        content = f.read()

    assert "chan" in content, f"The Go program {go_file} does not appear to use channels ('chan' keyword missing)."
    assert re.search(r'\bgo\s+', content), f"The Go program {go_file} does not appear to use goroutines ('go' keyword missing)."