# test_final_state.py

import os
import json
import sys
import importlib.util

def test_benchmark_report_exists_and_valid():
    report_path = "/home/user/ci_env/benchmark_report.json"
    assert os.path.isfile(report_path), f"Benchmark report {report_path} was not created."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "benchmark_report.json is not valid JSON."

    assert "successful_requests" in data, "Missing 'successful_requests' in benchmark report."
    assert data["successful_requests"] == 100, f"Expected 100 successful_requests, got {data['successful_requests']}."

    assert "total_time_ms" in data, "Missing 'total_time_ms' in benchmark report."
    assert isinstance(data["total_time_ms"], (int, float)), "'total_time_ms' must be a number."
    assert data["total_time_ms"] > 0, "'total_time_ms' must be greater than 0."

def test_nginx_config_websocket_upgrade():
    conf_path = "/home/user/ci_env/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "proxy_set_header Upgrade $http_upgrade;" in content or "proxy_set_header Upgrade $http_upgrade" in content, \
        "nginx.conf is missing the 'proxy_set_header Upgrade $http_upgrade;' directive."
    assert "proxy_set_header Connection" in content, \
        "nginx.conf is missing the 'proxy_set_header Connection' directive."

def test_emulator_stack_machine_logic():
    emulator_path = "/home/user/ci_env/emulator.py"
    assert os.path.isfile(emulator_path), f"File {emulator_path} does not exist."

    # Dynamically import the emulator module
    spec = importlib.util.spec_from_file_location("emulator", emulator_path)
    emulator = importlib.util.module_from_spec(spec)
    sys.modules["emulator"] = emulator
    try:
        spec.loader.exec_module(emulator)
    except Exception as e:
        assert False, f"Failed to import emulator.py: {e}"

    assert hasattr(emulator, "process_command"), "emulator.py is missing 'process_command' function."

    # Test valid cases
    assert emulator.process_command("PUSH 5 PUSH 10 ADD PUSH 2 MUL") == "30", \
        "process_command failed on 'PUSH 5 PUSH 10 ADD PUSH 2 MUL'."
    assert emulator.process_command("PUSH 42") == "42", \
        "process_command failed on 'PUSH 42'."
    assert emulator.process_command("PUSH 2 PUSH 3 PUSH 4 MUL ADD") == "14", \
        "process_command failed on 'PUSH 2 PUSH 3 PUSH 4 MUL ADD'."

    # Test invalid cases
    assert emulator.process_command("ADD") == "ERROR", \
        "process_command should return 'ERROR' for invalid stack operations (e.g., empty stack ADD)."
    assert emulator.process_command("PUSH 1 ADD") == "ERROR", \
        "process_command should return 'ERROR' for invalid stack operations (e.g., not enough elements for ADD)."
    assert emulator.process_command("PUSH A") == "ERROR" or emulator.process_command("PUSH A") == "ERROR", \
        "process_command should handle invalid integers gracefully."