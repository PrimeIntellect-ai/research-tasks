# test_final_state.py

import os
import subprocess
import json
import pytest

def test_audio_result_file():
    """Verify the audio_result.txt contains the correct result."""
    result_path = "/home/user/audio_result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."
    with open(result_path, "r") as f:
        content = f.read().strip()
    assert content in ["18", "18.0"], f"Expected 18 or 18.0 in {result_path}, got '{content}'"

def test_transcript_file():
    """Verify the transcript file exists and has content."""
    transcript_path = "/home/user/transcript.txt"
    assert os.path.isfile(transcript_path), f"File {transcript_path} does not exist."
    with open(transcript_path, "r") as f:
        content = f.read().strip().lower()
    assert "ten" in content or "10" in content, "Transcript does not seem to contain the correct transcription."

def test_shared_library_symbol():
    """Verify the math_core shared library exposes evaluate_expr."""
    # Look for the .so file in debug or release
    debug_so = "/home/user/math_core/target/debug/libmath_core.so"
    release_so = "/home/user/math_core/target/release/libmath_core.so"

    so_path = None
    if os.path.isfile(debug_so):
        so_path = debug_so
    elif os.path.isfile(release_so):
        so_path = release_so

    assert so_path is not None, "libmath_core.so not found in target/debug or target/release."

    result = subprocess.run(["nm", so_path], capture_output=True, text=True)
    assert "evaluate_expr" in result.stdout, f"Symbol 'evaluate_expr' not found in {so_path}"

def test_grpc_authorized_request():
    """Verify the gRPC service returns the correct result for an authorized request."""
    cmd = [
        "grpcurl",
        "-plaintext",
        "-H", "authorization: Bearer MIGRATE_PY3_TOKEN",
        "-d", '{"expression": "4 * 4 - 2"}',
        "127.0.0.1:50051",
        "calculator.Calculator/Evaluate"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    except FileNotFoundError:
        pytest.fail("grpcurl is not installed or not in PATH.")
    except subprocess.TimeoutExpired:
        pytest.fail("gRPC request timed out.")

    assert result.returncode == 0, f"gRPC request failed: {result.stderr}"
    try:
        response_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse gRPC response as JSON: {result.stdout}")

    assert "result" in response_data, f"Response missing 'result' field: {response_data}"
    assert float(response_data["result"]) == 14.0, f"Expected result 14.0, got {response_data['result']}"

def test_grpc_unauthorized_request():
    """Verify the gRPC service rejects requests without the correct authorization token."""
    cmd = [
        "grpcurl",
        "-plaintext",
        "-d", '{"expression": "4 * 4 - 2"}',
        "127.0.0.1:50051",
        "calculator.Calculator/Evaluate"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    except FileNotFoundError:
        pytest.fail("grpcurl is not installed or not in PATH.")
    except subprocess.TimeoutExpired:
        pytest.fail("gRPC request timed out.")

    assert result.returncode != 0, "Expected unauthorized gRPC request to fail, but it succeeded."
    assert "Unauthenticated" in result.stderr or "PermissionDenied" in result.stderr or "Unauthenticated" in result.stdout or "PermissionDenied" in result.stdout or "unauthenticated" in result.stderr.lower() or "permission" in result.stderr.lower(), f"Expected authentication error, got: {result.stderr}"