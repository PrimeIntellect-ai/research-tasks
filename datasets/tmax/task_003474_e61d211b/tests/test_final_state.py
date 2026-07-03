# test_final_state.py
import os
import hashlib

def test_payload_bin_exists_and_content():
    payload_path = "/home/user/storage/payload.bin"
    assert os.path.isfile(payload_path), f"File {payload_path} does not exist."

    expected_hex = (
        "5468697320697320612073656372"
        "65742062696e617279207061796c"
        "6f61642068696464656e20696e20"
        "746865206c6f67732e0a"
    )
    expected_bytes = bytes.fromhex(expected_hex)

    with open(payload_path, "rb") as f:
        content = f.read()

    assert content == expected_bytes, "The content of payload.bin does not match the expected decoded binary data."

def test_cleaned_app_log_exists_and_content():
    log_path = "/home/user/storage/cleaned_app.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    expected_content = (
        "[2023-10-24 08:12:01] INFO System startup initiated.\n"
        "[2023-10-24 08:12:05] WARN Storage latency detected on /dev/sda1.\n"
        "[2023-10-24 08:15:30] ERROR Fatal kernel panic simulated.\n"
        "[DUMP EXTRACTED TO PAYLOAD.BIN]\n"
        "[2023-10-24 08:16:00] INFO Rebooting system...\n"
        "[2023-10-24 08:16:15] INFO System back online.\n"
    )

    with open(log_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), "The content of cleaned_app.log does not match the expected output."