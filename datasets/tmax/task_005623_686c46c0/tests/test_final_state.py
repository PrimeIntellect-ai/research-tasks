# test_final_state.py

import os
import json
import pytest

SYSDEBUG_DIR = "/home/user/sysdebug"

def test_analyze_py_exists():
    path = os.path.join(SYSDEBUG_DIR, "analyze.py")
    assert os.path.isfile(path), f"{path} is missing."

def test_missing_symbols_json():
    path = os.path.join(SYSDEBUG_DIR, "missing_symbols.json")
    assert os.path.isfile(path), f"{path} is missing."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file.")

    assert isinstance(data, dict), f"JSON content in {path} must be a dictionary."

    # Check for target symbols
    assert "libgamma.so" in data, "libgamma.so missing from JSON."
    assert "fetch_config_value" in data["libgamma.so"], "fetch_config_value missing from libgamma.so symbols."

    assert "libbeta.so" in data, "libbeta.so missing from JSON."
    assert "g" in data["libbeta.so"], "'g' missing from libbeta.so symbols."

    assert "libalpha.so" in data, "libalpha.so missing from JSON."
    assert "b" in data["libalpha.so"], "'b' missing from libalpha.so symbols."

def test_fixture_files_exist():
    c_path = os.path.join(SYSDEBUG_DIR, "fixture.c")
    so_path = os.path.join(SYSDEBUG_DIR, "libfixture.so")

    assert os.path.isfile(c_path), f"{c_path} is missing."
    assert os.path.isfile(so_path), f"{so_path} is missing."

def test_result_txt():
    path = os.path.join(SYSDEBUG_DIR, "result.txt")
    assert os.path.isfile(path), f"{path} is missing."

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "Success: 89", f"Expected 'Success: 89' in result.txt, but got '{content}'."