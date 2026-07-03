# test_final_state.py

import os
import re
import stat
import pytest

def test_encoder_compiled():
    encoder_path = "/home/user/waf_encoder/encoder"
    assert os.path.isfile(encoder_path), f"Compiled binary not found at {encoder_path}"
    assert os.access(encoder_path, os.X_OK), f"Binary {encoder_path} is not executable"

def test_test_harness_exists_and_executable():
    harness_path = "/home/user/test_harness.sh"
    assert os.path.isfile(harness_path), f"Test harness script not found at {harness_path}"
    assert os.access(harness_path, os.X_OK), f"Test harness {harness_path} is not executable"

def test_payload_dat_correct():
    payload_dat_path = "/home/user/payload.dat"
    assert os.path.isfile(payload_dat_path), f"Payload file not found at {payload_dat_path}"

    with open(payload_dat_path, "r") as f:
        content = f.read()

    assert len(content) == 100000, f"payload.dat should be exactly 100,000 bytes, got {len(content)}"
    assert content == "X" * 100000, "payload.dat does not contain exactly 100,000 'X' characters"

def test_payload_ser_correct():
    payload_ser_path = "/home/user/payload.ser"
    assert os.path.isfile(payload_ser_path), f"Serialized payload not found at {payload_ser_path}"

    with open(payload_ser_path, "r") as f:
        content = f.read()

    expected_prefix = "100000:"
    assert content.startswith(expected_prefix), "payload.ser does not start with '100000:'"
    assert content[len(expected_prefix):] == "X" * 100000, "payload.ser data portion is incorrect"

def test_payload_enc_correct():
    payload_enc_path = "/home/user/payload.enc"
    assert os.path.isfile(payload_enc_path), f"Encoded payload not found at {payload_enc_path}"

    with open(payload_enc_path, "r") as f:
        content = f.read().strip()

    assert len(content) == 200000, f"payload.enc should contain 200,000 hex characters, got {len(content)}"
    assert content == "58" * 100000, "payload.enc does not correctly hex-encode the payload"

def test_qa_log_correct():
    qa_log_path = "/home/user/qa_log.txt"
    assert os.path.isfile(qa_log_path), f"QA log file not found at {qa_log_path}"

    with open(qa_log_path, "r") as f:
        content = f.read()

    assert "TEST: WAF_ENCODER" in content, "qa_log.txt missing 'TEST: WAF_ENCODER'"
    assert "STATUS: PASS" in content, "qa_log.txt missing 'STATUS: PASS'"

    time_match = re.search(r"TIME_MS:\s*\d+", content)
    assert time_match is not None, "qa_log.txt missing 'TIME_MS: [Calculated Duration]'"