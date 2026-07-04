# test_final_state.py

import os
import json
import ctypes
import pytest

def test_c_source_and_library_exist():
    """Check if the C source file and compiled shared library exist."""
    c_file = '/home/user/test_env/telemetry.c'
    so_file = '/home/user/test_env/libtelemetry.so'

    assert os.path.isfile(c_file), f"C source file {c_file} does not exist."
    assert os.path.isfile(so_file), f"Shared library {so_file} does not exist."

def test_haproxy_config_exists():
    """Check if the HAProxy configuration file exists."""
    cfg_file = '/home/user/test_env/haproxy.cfg'
    assert os.path.isfile(cfg_file), f"HAProxy config file {cfg_file} does not exist."

def test_result_json_content():
    """Check if the result.json file exists and contains the correct decoded output."""
    result_file = '/home/user/test_env/result.json'
    assert os.path.isfile(result_file), f"Result file {result_file} does not exist."

    with open(result_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_file} does not contain valid JSON.")

    assert "id" in data, "JSON response is missing the 'id' field."
    assert "text" in data, "JSON response is missing the 'text' field."

    assert data["id"] == 5, f"Expected id 5, got {data['id']}"
    assert data["text"] == "hello world!", f"Expected text 'hello world!', got '{data['text']}'"

def test_libtelemetry_abi():
    """Directly test the compiled shared library to ensure ABI compliance and correctness."""
    so_file = '/home/user/test_env/libtelemetry.so'
    if not os.path.isfile(so_file):
        pytest.skip("Shared library not found, skipping ABI test.")

    class Record(ctypes.Structure):
        _fields_ = [
            ("record_id", ctypes.c_uint32),
            ("decoded_text", ctypes.c_char * 64)
        ]

    try:
        lib = ctypes.CDLL(so_file)
    except Exception as e:
        pytest.fail(f"Failed to load shared library {so_file}: {e}")

    lib.process_record.argtypes = [ctypes.c_char_p, ctypes.POINTER(Record)]
    lib.process_record.restype = ctypes.c_int

    record = Record()

    # Test with the provided hex input
    hex_input = b"050000007572797962206a6265797121"
    res = lib.process_record(hex_input, ctypes.byref(record))

    assert res == 0, "process_record returned a non-zero status for valid input."
    assert record.record_id == 5, f"Expected record_id 5, got {record.record_id}"

    decoded_text = record.decoded_text.decode('utf-8')
    assert decoded_text == "hello world!", f"Expected decoded_text 'hello world!', got '{decoded_text}'"