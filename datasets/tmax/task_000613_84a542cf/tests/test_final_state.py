# test_final_state.py

import os
import pytest

def test_bad_payload_extracted():
    payload_path = "/home/user/bad_payload.json"
    assert os.path.isfile(payload_path), f"File not found: {payload_path}"

    with open(payload_path, "rb") as f:
        content = f.read()

    expected_bytes = b'{"session":"req_8f7b2","user_id":42,"data":"bad\xffdata"}'
    assert content == expected_bytes, f"Content of {payload_path} does not match the exact expected byte sequence."

def test_cargo_toml_fixed():
    cargo_path = "/home/user/ticket_app/Cargo.toml"
    assert os.path.isfile(cargo_path), f"File not found: {cargo_path}"

    with open(cargo_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "serde" in content, "serde dependency is missing in Cargo.toml."
    assert "derive" in content, "The 'derive' feature for serde is missing in Cargo.toml."

def test_session_extracted():
    session_path = "/home/user/session.txt"
    assert os.path.isfile(session_path), f"File not found: {session_path}. Did you run the Rust application?"

    with open(session_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    assert content == "req_8f7b2", f"Content of {session_path} is incorrect. Expected 'req_8f7b2', got '{content}'."

def test_main_rs_modified():
    main_path = "/home/user/ticket_app/src/main.rs"
    assert os.path.isfile(main_path), f"File not found: {main_path}"

    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Hello, world!" not in content or len(content.splitlines()) > 5, "main.rs does not appear to have been implemented."