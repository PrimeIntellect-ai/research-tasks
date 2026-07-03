# test_final_state.py
import os
import pytest

def test_recovered_requests_log():
    expected_content = """REQ A
REQ B
PROCESS_WINDOW
REQ C
REQ D
REQ E
PROCESS_WINDOW
REQ F
REQ G
REQ H
REQ I
PROCESS_WINDOW
"""
    log_path = "/home/user/recovered_requests.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert content.strip() == expected_content.strip(), f"Content of {log_path} does not match the expected recovered logs."

def test_minimal_crash_txt():
    crash_path = "/home/user/minimal_crash.txt"
    assert os.path.isfile(crash_path), f"File {crash_path} does not exist."
    with open(crash_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 4, f"{crash_path} should contain exactly 4 lines."
    req_count = sum(1 for line in lines if line.startswith("REQ"))
    process_count = sum(1 for line in lines if line == "PROCESS_WINDOW")

    assert req_count == 3, "Minimal crash file should contain exactly 3 REQ lines."
    assert process_count == 1, "Minimal crash file should contain exactly 1 PROCESS_WINDOW line."
    assert lines[-1] == "PROCESS_WINDOW", "The last line of the minimal crash file should be PROCESS_WINDOW."

def test_rust_bug_fixed():
    main_rs = "/home/user/service_repo/src/main.rs"
    assert os.path.isfile(main_rs), f"File {main_rs} does not exist."
    with open(main_rs, "r") as f:
        content = f.read()

    assert "&buffer[i..=chunk_end]" not in content, "The off-by-one bug (&buffer[i..=chunk_end]) is still present in src/main.rs."
    assert "&buffer[i..chunk_end]" in content, "The fix (&buffer[i..chunk_end]) was not found in src/main.rs."

def test_processor_output():
    output_path = "/home/user/processor_output.txt"
    assert os.path.isfile(output_path), f"File {output_path} does not exist."
    with open(output_path, "r") as f:
        content = f.read()

    assert "Processed: 6" in content, f"Expected 'Processed: 6' in {output_path}, but got: {content}"