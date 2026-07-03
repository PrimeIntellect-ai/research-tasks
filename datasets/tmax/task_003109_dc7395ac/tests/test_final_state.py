# test_final_state.py
import os
import pytest

def test_build_script_cross_compilation():
    build_script = "/home/user/project/build.sh"
    assert os.path.isfile(build_script), "build.sh is missing."

    with open(build_script, "r") as f:
        content = f.read()

    assert "aarch64-linux-gnu-gcc" in content, "build.sh does not use aarch64-linux-gnu-gcc for compilation."
    assert "aarch64-linux-gnu-ar" in content, "build.sh does not use aarch64-linux-gnu-ar for archiving."

def test_cargo_config_linker():
    cargo_config = "/home/user/project/.cargo/config.toml"
    assert os.path.isfile(cargo_config), ".cargo/config.toml is missing."

    with open(cargo_config, "r") as f:
        content = f.read()

    assert "target.aarch64-unknown-linux-gnu" in content, ".cargo/config.toml does not configure target.aarch64-unknown-linux-gnu."
    assert "linker" in content and "aarch64-linux-gnu-gcc" in content, ".cargo/config.toml does not set the correct linker."

def test_test_ws_script():
    test_script = "/home/user/project/test_ws.sh"
    assert os.path.isfile(test_script), "test_ws.sh is missing."
    assert os.access(test_script, os.X_OK), "test_ws.sh is not executable."

    with open(test_script, "r") as f:
        content = f.read()

    assert "curl" in content, "test_ws.sh does not use curl."
    assert "Upgrade: websocket" in content or "upgrade: websocket" in content.lower(), "test_ws.sh does not contain WebSocket upgrade headers."
    assert "ws://localhost:8080/stream" in content, "test_ws.sh does not target the correct WebSocket URL."

    payload = '{"command": "process", "payload": [1, 2, 3, 4]}'
    # Remove spaces for robust checking
    compact_payload = payload.replace(" ", "")
    compact_content = content.replace(" ", "")
    assert compact_payload in compact_content, "test_ws.sh does not send the correct JSON payload."

    assert "/home/user/ws_test_output.log" in content, "test_ws.sh does not save output to /home/user/ws_test_output.log."