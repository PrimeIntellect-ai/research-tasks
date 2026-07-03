# test_final_state.py

import os
import subprocess
import json
import re
import ctypes
import pytest

def test_server_status_log():
    log_path = "/home/user/workspace/server_status.log"
    assert os.path.isfile(log_path), f"Log file not found: {log_path}"
    with open(log_path, "r") as f:
        content = f.read()
    assert "SERVER READY" in content, f"Log file does not contain 'SERVER READY'. Content: {content}"

def test_test_ecc_bin():
    bin_path = "/home/user/workspace/test_ecc_bin"
    assert os.path.isfile(bin_path), f"Test binary not found: {bin_path}"
    assert os.access(bin_path, os.X_OK), f"Test binary is not executable: {bin_path}"

    result = subprocess.run([bin_path], capture_output=True, text=True)
    assert result.returncode == 0, f"RapidCheck test failed. Output:\n{result.stdout}\n{result.stderr}"

def test_grpc_verify_asset():
    proto_path = "/home/user/workspace/build_gate.proto"
    assert os.path.isfile(proto_path), f"Proto file not found: {proto_path}"

    # Calculate expected CRC using the provided libecc.so
    lib_path = "/app/lib/libecc.so"
    assert os.path.isfile(lib_path), f"libecc.so not found: {lib_path}"

    ecc_lib = ctypes.CDLL(lib_path)
    ecc_lib.calculate_asset_crc.argtypes = [ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
    ecc_lib.calculate_asset_crc.restype = ctypes.c_uint32

    wav_path = "/app/assets/config_memo.wav"
    assert os.path.isfile(wav_path), f"WAV file not found: {wav_path}"

    with open(wav_path, "rb") as f:
        wav_data = f.read()

    buffer = (ctypes.c_uint8 * len(wav_data)).from_buffer_copy(wav_data)
    expected_crc = ecc_lib.calculate_asset_crc(buffer, len(wav_data))

    # Use grpcurl to call the service
    # We use the proto file since reflection might not be enabled
    cmd = [
        "grpcurl",
        "-plaintext",
        "-proto", proto_path,
        "-d", json.dumps({"file_path": wav_path}),
        "127.0.0.1:50051",
        "AudioBuildGate/VerifyAsset"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"grpcurl failed to call VerifyAsset. Error:\n{result.stderr}"

    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse gRPC response as JSON. Output:\n{result.stdout}")

    assert "transcript" in response, "Response missing 'transcript' field"
    assert "checksum" in response, "Response missing 'checksum' field"
    assert "isValid" in response or "is_valid" in response, "Response missing 'is_valid' field"

    # Verify transcript
    transcript = response["transcript"].lower()
    transcript = re.sub(r'[^\w\s]', '', transcript)
    expected_transcript = "the build token is alpha bravo charlie niner"
    assert expected_transcript in transcript, f"Transcript does not match. Expected to contain: '{expected_transcript}', Got: '{transcript}'"

    # Verify checksum
    actual_checksum = int(response["checksum"])
    assert actual_checksum == expected_crc, f"Checksum mismatch. Expected: {expected_crc}, Got: {actual_checksum}"

    # Verify is_valid
    is_valid = response.get("isValid", response.get("is_valid"))
    assert is_valid is True, f"is_valid flag should be true, got {is_valid}"