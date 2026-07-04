# test_final_state.py

import os
import urllib.request
import urllib.error
import subprocess
import json
import pytest

def test_patch_applied():
    test_runner_path = '/home/user/release_prep/tests/test_runner.cpp'
    assert os.path.isfile(test_runner_path), f"File {test_runner_path} is missing."
    with open(test_runner_path, 'r') as f:
        content = f.read()
    assert "// Added mock fixture initialization" in content, "The patch was not applied to tests/test_runner.cpp."

def test_makefile_fixed():
    makefile_path = '/home/user/release_prep/Makefile'
    assert os.path.isfile(makefile_path), f"File {makefile_path} is missing."
    with open(makefile_path, 'r') as f:
        content = f.read()

    # Check for threading flag
    assert "-pthread" in content, "The Makefile is missing the -pthread flag."

    # Check if run_tests links config_parser.o
    lines = content.splitlines()
    run_tests_cmd = ""
    for i, line in enumerate(lines):
        if line.startswith("run_tests:"):
            if i + 1 < len(lines):
                run_tests_cmd = lines[i+1]
            break

    assert "src/config_parser.o" in run_tests_cmd or "config_parser.o" in run_tests_cmd, \
        "The Makefile does not correctly link config_parser.o for the run_tests target."

def test_cpp_bugs_fixed():
    config_parser_path = '/home/user/release_prep/src/config_parser.cpp'
    assert os.path.isfile(config_parser_path), f"File {config_parser_path} is missing."
    with open(config_parser_path, 'r') as f:
        config_content = f.read()
    assert '"service_port"' not in config_content, "The JSON deserialization bug in config_parser.cpp (looking for 'service_port') was not fixed."
    assert '"port"' in config_content, "config_parser.cpp should look for the correct key 'port'."

    main_path = '/home/user/release_prep/src/main.cpp'
    assert os.path.isfile(main_path), f"File {main_path} is missing."
    with open(main_path, 'r') as f:
        main_content = f.read()
    assert "const std::string& getStatusMessage()" not in main_content, "The lifetime bug in main.cpp (returning a dangling reference) was not fixed."
    assert "std::string getStatusMessage()" in main_content, "getStatusMessage() in main.cpp should return std::string by value."

def test_test_results_log():
    log_path = '/home/user/test_results.log'
    assert os.path.isfile(log_path), f"The test results log {log_path} is missing."
    with open(log_path, 'r') as f:
        content = f.read().strip()
    assert "TESTS PASSED" in content, "The test_results.log does not indicate that the tests passed."

def test_deploy_ready_txt():
    deploy_path = '/home/user/deploy_ready.txt'
    assert os.path.isfile(deploy_path), f"The deployment ready file {deploy_path} is missing."
    with open(deploy_path, 'r') as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
        assert data.get("status") == "ok", "The deploy_ready.txt JSON does not have 'status': 'ok'."
        assert data.get("version") == "1.2.0", "The deploy_ready.txt JSON does not have 'version': '1.2.0'."
    except json.JSONDecodeError:
        pytest.fail(f"The file {deploy_path} does not contain valid JSON. Content: {content}")

def test_api_server_running_and_serving():
    try:
        req = urllib.request.Request("http://127.0.0.1:9000/")
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)
            assert data.get("status") == "ok"
    except Exception as e:
        pytest.fail(f"Could not connect to the api_server on 127.0.0.1:9000 or it returned invalid data. Error: {e}")

def test_haproxy_running_and_proxying():
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/status")
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8')
            data = json.loads(body)
            assert data.get("status") == "ok"
    except Exception as e:
        pytest.fail(f"Could not connect to HAProxy on 127.0.0.1:8080 or it did not proxy correctly. Error: {e}")

def test_background_processes_running():
    try:
        ps_output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
        assert 'api_server' in ps_output, "api_server is not running in the background."
        assert 'haproxy' in ps_output, "haproxy is not running in the background."
    except Exception as e:
        pytest.fail(f"Failed to check running processes: {e}")