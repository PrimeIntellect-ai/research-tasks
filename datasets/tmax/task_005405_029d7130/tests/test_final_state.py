# test_final_state.py

import os
import sys
import importlib.util
import pytest

BUILD_DIR = "/home/user/build_system"
SCHEMA_FILE = os.path.join(BUILD_DIR, "schema.proto")
BUILD_SCRIPT = os.path.join(BUILD_DIR, "build.sh")
PAYLOAD_FILE = os.path.join(BUILD_DIR, "payload.bin")
BENCH_LOG = os.path.join(BUILD_DIR, "bench.log")

def test_schema_proto_exists_and_valid():
    assert os.path.exists(SCHEMA_FILE), f"Schema file not found at {SCHEMA_FILE}"
    with open(SCHEMA_FILE, "r") as f:
        content = f.read()

    assert "syntax" in content and "proto3" in content, "Schema must use proto3 syntax."
    assert "message ConfigRequest" in content, "Schema missing 'message ConfigRequest'."
    assert "message ConfigResponse" in content, "Schema missing 'message ConfigResponse'."
    assert "service Configurator" in content, "Schema missing 'service Configurator'."
    assert "rpc UpdateConfig" in content, "Schema missing 'rpc UpdateConfig'."

def test_build_script_exists_and_executable():
    assert os.path.exists(BUILD_SCRIPT), f"Build script not found at {BUILD_SCRIPT}"
    assert os.access(BUILD_SCRIPT, os.X_OK), f"Build script at {BUILD_SCRIPT} is not executable."

def test_payload_exists():
    assert os.path.exists(PAYLOAD_FILE), f"Payload file not found at {PAYLOAD_FILE}"

def test_bench_log_exists_and_contains_timing():
    assert os.path.exists(BENCH_LOG), f"Benchmark log not found at {BENCH_LOG}"
    with open(BENCH_LOG, "r") as f:
        content = f.read().lower()

    # The 'time' command outputs real, user, sys
    has_timing = "real" in content or "user" in content or "sys" in content
    assert has_timing, f"Benchmark log {BENCH_LOG} does not appear to contain 'time' command output."

def test_payload_content():
    # Ensure payload exists
    assert os.path.exists(PAYLOAD_FILE), "Payload file missing, cannot verify content."

    # Import the generated schema_pb2.py
    pb2_path = os.path.join(BUILD_DIR, "schema_pb2.py")
    assert os.path.exists(pb2_path), f"Generated python bindings not found at {pb2_path}"

    sys.path.insert(0, BUILD_DIR)
    try:
        import schema_pb2

        with open(PAYLOAD_FILE, "rb") as f:
            data = f.read()

        req = schema_pb2.ConfigRequest()
        req.ParseFromString(data)

        assert getattr(req, "key", None) == "max_workers", f"Expected key 'max_workers', got {getattr(req, 'key', None)}"
        assert getattr(req, "value", None) == 42, f"Expected value 42, got {getattr(req, 'value', None)}"
    except ImportError:
        pytest.fail("Failed to import schema_pb2. Make sure it was generated correctly.")
    except Exception as e:
        pytest.fail(f"Failed to parse payload.bin or verify contents: {e}")
    finally:
        sys.path.pop(0)