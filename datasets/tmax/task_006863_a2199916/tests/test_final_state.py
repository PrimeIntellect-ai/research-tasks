# test_final_state.py

import os
import socket
import pytest

def test_rust_code_fixed():
    # Check main.rs
    main_path = "/home/user/ws-ingest/src/main.rs"
    assert os.path.isfile(main_path), f"{main_path} is missing."
    with open(main_path, "r") as f:
        main_content = f.read()
    assert ".await" in main_content and "ws_stream.next()" in main_content, "The missing .await bug in main.rs was not fixed."

    # Check parser.rs
    parser_path = "/home/user/ws-ingest/src/parser.rs"
    assert os.path.isfile(parser_path), f"{parser_path} is missing."
    with open(parser_path, "r") as f:
        parser_content = f.read()
    assert "u32" in parser_content and "String" not in parser_content.split("pub checksum:")[1].split(",")[0], "The checksum type in parser.rs was not changed to u32."

    # Check checksum.rs
    checksum_path = "/home/user/ws-ingest/src/checksum.rs"
    assert os.path.isfile(checksum_path), f"{checksum_path} is missing."
    with open(checksum_path, "r") as f:
        checksum_content = f.read()
    assert "as_bytes()" in checksum_content, "The hasher.update call in checksum.rs was not fixed to use .as_bytes()."

def test_nginx_config():
    proxy_conf_path = "/home/user/proxy.conf"
    assert os.path.isfile(proxy_conf_path), f"Nginx config {proxy_conf_path} is missing."
    with open(proxy_conf_path, "r") as f:
        content = f.read()

    assert "127.0.0.1:8080" in content or " 8080" in content, "Nginx is not configured to listen on port 8080."
    assert "proxy_pass" in content and "9090" in content, "Nginx is not configured to proxy_pass to port 9090."
    assert "Upgrade" in content, "Nginx is not configured to handle WebSocket Upgrade headers."

def test_services_running():
    # Check if port 9090 (Rust server) is open
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 9090))
        assert result == 0, "The Rust WebSocket server is not listening on 127.0.0.1:9090."

    # Check if port 8080 (Nginx) is open
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex(('127.0.0.1', 8080))
        assert result == 0, "The Nginx reverse proxy is not listening on 127.0.0.1:8080."

def test_python_script_exists():
    script_path = "/home/user/test_ws.py"
    assert os.path.isfile(script_path), f"The Python test script {script_path} is missing."

def test_result_log():
    log_path = "/home/user/test_result.log"
    assert os.path.isfile(log_path), f"The test result log {log_path} is missing. Did the Python script run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "SUCCESS: Checksum verified" in content, f"The test result log does not contain the expected success message. Found: {content}"