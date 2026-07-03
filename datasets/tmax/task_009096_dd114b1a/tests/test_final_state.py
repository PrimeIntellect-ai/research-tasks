# test_final_state.py

import os
import pytest

def test_run_sh_updated():
    run_sh_path = "/home/user/ingester_diag/run.sh"
    assert os.path.isfile(run_sh_path), f"{run_sh_path} does not exist."

    with open(run_sh_path, "r") as f:
        content = f.read()

    assert "TARGET_PORT=9000" in content, "run.sh does not have TARGET_PORT updated to 9000."
    assert "tshark" in content, "run.sh does not use tshark to extract payloads."
    assert "cargo run" in content, "run.sh does not pipe to 'cargo run'."

def test_main_rs_fixed():
    main_rs_path = "/home/user/ingester_diag/ingester/src/main.rs"
    assert os.path.isfile(main_rs_path), f"{main_rs_path} does not exist."

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "String::from_utf8(bytes).unwrap()" not in content, "main.rs still contains the panic-inducing unwrap()."
    # We don't strictly assert the exact replacement method, but we expect it to be fixed.

def test_recovered_logs():
    logs_path = "/home/user/ingester_diag/recovered_logs.txt"
    assert os.path.isfile(logs_path), f"The file {logs_path} was not created."

    with open(logs_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 log lines, found {len(lines)}."

    assert lines[0] == "LOG: INFO: System start", "First log line does not match expected output."
    assert "LOG: WARN: Disk" in lines[1] and "error" in lines[1], "Second log line does not match expected output format."
    assert lines[2] == "LOG: INFO: System stop", "Third log line does not match expected output."

    # Check that the invalid byte was replaced, typically with the Unicode replacement character
    assert "\ufffd" in lines[1] or "?" in lines[1] or lines[1] == "LOG: WARN: Disk  error", "The invalid UTF-8 byte was not gracefully handled."