# test_final_state.py

import os
import json
import pytest

def test_libintegrate_so_exists_and_is_elf():
    """Test that the compiled C shared library exists and is an ELF file."""
    so_path = "/home/user/libintegrate.so"
    assert os.path.isfile(so_path), f"Shared library {so_path} does not exist. Did you compile the Go code?"

    with open(so_path, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"File {so_path} is not a valid ELF binary."

def test_result_json_exists_and_correct():
    """Test that test_result.json exists and contains the exact expected values."""
    json_path = "/home/user/test_result.json"
    assert os.path.isfile(json_path), f"JSON result file {json_path} does not exist. Did you run the Python script?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "module" in data, "Key 'module' missing from JSON."
    assert data["module"] == "libintegrate.so", f"Expected module 'libintegrate.so', got {data['module']}."

    assert "steps" in data, "Key 'steps' missing from JSON."
    assert data["steps"] == 1000000, f"Expected steps 1000000, got {data['steps']}."

    assert "result" in data, "Key 'result' missing from JSON."
    assert isinstance(data["result"], float), "Result should be a float."
    assert data["result"] == 3.141593, f"Expected result 3.141593, got {data['result']}."