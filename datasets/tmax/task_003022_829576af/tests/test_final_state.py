# test_final_state.py

import os
import json
import pytest

def test_config_json_fixed():
    config_path = "/home/user/service_app/config.json"
    assert os.path.isfile(config_path), f"{config_path} is missing"
    with open(config_path, "r") as f:
        config = json.load(f)

    # The task asks to bind to the local loopback IPv4 address
    assert config.get("host") == "127.0.0.1", "config.json does not have the correct loopback host (127.0.0.1)"
    assert config.get("port") == 9090, "config.json port should remain 9090"
    assert config.get("log_dir") == "/home/user/logs", "config.json log_dir should remain /home/user/logs"

def test_log_directory_created():
    log_dir = "/home/user/logs"
    assert os.path.isdir(log_dir), f"{log_dir} directory was not created"

def test_log_file_created_and_contains_message():
    log_file = "/home/user/logs/service.log"
    assert os.path.isfile(log_file), f"{log_file} was not created. Did the service run successfully?"

    with open(log_file, "r") as f:
        content = f.read()

    assert "[INFO] Server started successfully. Token: X9A4B2Z1V" in content, "Log file does not contain the expected startup message"

def test_solution_file_correct():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"{solution_path} is missing"

    with open(solution_path, "r") as f:
        content = f.read().strip()

    assert content == "X9A4B2Z1V", f"Expected token 'X9A4B2Z1V' in {solution_path}, but got '{content}'"

def test_main_rs_not_modified():
    main_rs_path = "/home/user/service_app/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} is missing"

    with open(main_rs_path, "r") as f:
        content = f.read()

    # Check key parts to ensure it wasn't tampered with rather than fixing the config
    assert "TcpListener::bind(&addr)" in content, "main.rs seems to have been modified (TcpListener::bind changed)"
    assert "Token: X9A4B2Z1V" in content, "main.rs seems to have been modified (Token changed)"
    assert "config.json" in content, "main.rs seems to have been modified (config.json reference changed)"