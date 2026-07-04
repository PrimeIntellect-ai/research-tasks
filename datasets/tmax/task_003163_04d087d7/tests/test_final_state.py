# test_final_state.py
import os
import stat
import pytest

TELEMETRY_DIR = "/home/user/telemetry"
PROTO_FILE = os.path.join(TELEMETRY_DIR, "telemetry.proto")
MAKEFILE = os.path.join(TELEMETRY_DIR, "Makefile")
C_FILE = os.path.join(TELEMETRY_DIR, "verify_checksum.c")
BIN_FILE = os.path.join(TELEMETRY_DIR, "verify_checksum")
PAYLOAD_FILE = os.path.join(TELEMETRY_DIR, "test_payload.bin")
RESULT_FILE = os.path.join(TELEMETRY_DIR, "pipeline_result.txt")

def test_telemetry_proto_patched():
    assert os.path.isfile(PROTO_FILE), f"File {PROTO_FILE} is missing."
    with open(PROTO_FILE, "r") as f:
        content = f.read()
    assert "string status = 2;" in content, "telemetry.proto is missing the 'status' field. Was the patch applied?"
    assert "service TelemetryService" in content, "telemetry.proto is missing the 'TelemetryService'. Was the patch applied?"

def test_c_code_and_makefile_fixed():
    assert os.path.isfile(C_FILE), f"File {C_FILE} is missing."
    with open(C_FILE, "r") as f:
        content = f.read()
    assert 'printf("Checksum: %d\\n", sum);' in content, "verify_checksum.c is still missing the semicolon."

    assert os.path.isfile(BIN_FILE), f"Executable {BIN_FILE} is missing. Did you run make?"
    st = os.stat(BIN_FILE)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {BIN_FILE} is not executable."

def test_payload_generated():
    assert os.path.isfile(PAYLOAD_FILE), f"File {PAYLOAD_FILE} is missing. Did you run generate_test_data.py?"
    with open(PAYLOAD_FILE, "rb") as f:
        content = f.read()

    # Expected protobuf serialization for device_id=101, status="ONLINE"
    # device_id: field 1, type int32 (varint) -> tag 0x08, value 101 (0x65)
    # status: field 2, type string (length-delimited) -> tag 0x12, length 6 (0x06), value "ONLINE"
    expected_bytes = b'\x08\x65\x12\x06ONLINE'

    assert content == expected_bytes, f"test_payload.bin does not contain the correct serialized data. Expected {expected_bytes.hex()}, got {content.hex()}."

def test_pipeline_result():
    assert os.path.isfile(RESULT_FILE), f"File {RESULT_FILE} is missing. Did you run the verify_checksum utility?"
    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    expected_sum = sum(b'\x08\x65\x12\x06ONLINE')
    expected_output = f"Checksum: {expected_sum}"

    assert expected_output in content, f"pipeline_result.txt does not contain the correct output. Expected '{expected_output}', got '{content}'."