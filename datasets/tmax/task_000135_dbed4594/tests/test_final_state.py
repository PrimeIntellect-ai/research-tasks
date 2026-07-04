# test_final_state.py

import json
import os
from pathlib import Path

def test_config_patched():
    config_path = Path("/home/user/ci_config.json")
    assert config_path.is_file(), f"Missing configuration file: {config_path}"

    with open(config_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {config_path} is not valid JSON"

    assert "services" in data, f"Missing 'services' key in {config_path}"
    assert "api" in data["services"], f"Missing 'api' service in {config_path}"

    api_version = data["services"]["api"]["version"]
    assert api_version == "2.2.1", f"Expected api version to be 2.2.1 after patching, but got {api_version}"

def test_build_order_log():
    log_path = Path("/home/user/build_order.log")
    assert log_path.is_file(), f"Missing build order log: {log_path}"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = ["cache", "database", "auth", "api", "frontend"]

    assert lines == expected_order, f"Build order is incorrect. Expected {expected_order}, got {lines}"

def test_makefile_structure():
    makefile_path = Path("/home/user/Makefile")
    assert makefile_path.is_file(), f"Missing Makefile: {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    lines = [line.rstrip() for line in content.splitlines()]

    # Check 'all' target
    expected_all_target = "all: cache database auth api frontend"
    assert any(line.startswith(expected_all_target) for line in lines), \
        f"Makefile is missing the correct 'all' target. Expected to find a line starting with: '{expected_all_target}'"

    # Check individual targets
    expected_services = {
        "cache": "2.0.0",
        "database": "3.0.1",
        "auth": "1.2.0",
        "api": "2.2.1",
        "frontend": "1.0.5"
    }

    for service, version in expected_services.items():
        target_line = f"{service}:"
        command_line = f"\t@echo \"Building {service} v{version}\""

        # Find the target line
        try:
            target_idx = lines.index(target_line)
        except ValueError:
            assert False, f"Makefile is missing target '{target_line}'"

        # Check if the next line is the correct command
        assert target_idx + 1 < len(lines), f"Makefile target '{target_line}' has no command"
        actual_command = lines[target_idx + 1]
        assert actual_command == command_line, \
            f"Incorrect command for target '{service}'. Expected '{command_line}', got '{actual_command}'"

    # Ensure analytics is NOT in the Makefile
    assert "analytics:" not in lines, "Makefile should not contain 'analytics' target as its dependencies are unmet"