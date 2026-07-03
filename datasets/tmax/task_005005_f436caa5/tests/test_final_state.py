# test_final_state.py
import json
import os
import pytest

def test_libtelemetry_built():
    assert os.path.exists("/home/user/build_pipeline/libtelemetry.so"), "libtelemetry.so was not built."

def test_main_import_order():
    main_path = "/home/user/build_pipeline/main.py"
    assert os.path.exists(main_path), "main.py is missing."
    with open(main_path, "r") as f:
        content = f.read()

    config_idx = content.find("import config")
    ffi_idx = content.find("import ffi_wrapper")

    assert config_idx != -1, "main.py is missing 'import config'"
    assert ffi_idx != -1, "main.py is missing 'import ffi_wrapper'"
    assert config_idx < ffi_idx, "config must be imported before ffi_wrapper in main.py to fix the import order bug."

def test_final_output_json():
    filepath = "/home/user/build_pipeline/final_output.json"
    assert os.path.exists(filepath), "final_output.json does not exist."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("final_output.json does not contain valid JSON.")

    assert isinstance(data, dict), "final_output.json should contain a JSON object."
    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("code") == 0, f"Expected code 0, got {data.get('code')}"