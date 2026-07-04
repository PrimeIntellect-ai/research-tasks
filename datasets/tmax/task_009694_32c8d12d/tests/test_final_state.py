# test_final_state.py

import os
import json
import subprocess
import pytest

APP_DIR = "/home/user/app"
BUILD_SCRIPT = os.path.join(APP_DIR, "build_and_test.sh")
RESULT_JSON = os.path.join(APP_DIR, "result.json")
INPUT_JSON = os.path.join(APP_DIR, "input.json")
ASM_HELPER_SO = os.path.join(APP_DIR, "libasm_helper.so")
RUST_TRANSFORM_SO = os.path.join(APP_DIR, "librust_transform.so")

def test_build_script_exists_and_executable():
    assert os.path.isfile(BUILD_SCRIPT), f"Build script {BUILD_SCRIPT} does not exist."
    assert os.access(BUILD_SCRIPT, os.X_OK), f"Build script {BUILD_SCRIPT} is not executable."

def test_build_and_test_execution():
    # Remove result.json if it exists to ensure the script generates it
    if os.path.exists(RESULT_JSON):
        os.remove(RESULT_JSON)

    result = subprocess.run(
        [BUILD_SCRIPT],
        cwd=APP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"build_and_test.sh failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_shared_libraries_generated():
    assert os.path.isfile(ASM_HELPER_SO), f"C shared library {ASM_HELPER_SO} was not generated."
    assert os.path.isfile(RUST_TRANSFORM_SO), f"Rust shared library {RUST_TRANSFORM_SO} was not copied to the app directory."

def test_result_json_correct():
    assert os.path.isfile(RESULT_JSON), f"Output file {RESULT_JSON} was not created."

    with open(INPUT_JSON, 'r') as f:
        input_data = json.load(f)

    with open(RESULT_JSON, 'r') as f:
        try:
            result_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULT_JSON} is not valid JSON.")

    assert isinstance(result_data, list), "result.json should contain a JSON array."
    assert len(result_data) == len(input_data), f"result.json should have {len(input_data)} items, got {len(result_data)}."

    # Compute expected results dynamically based on input.json
    expected_results = []
    for item in input_data:
        payload = item.get("payload", "")
        reversed_payload = payload[::-1]

        # Compute XOR checksum
        checksum = 0
        for char in reversed_payload:
            checksum ^= ord(char)

        expected_results.append({
            "id": item.get("id"),
            "reversed": reversed_payload,
            "checksum": checksum
        })

    # Compare each item
    for expected, actual in zip(expected_results, result_data):
        assert actual.get("id") == expected["id"], f"Expected id {expected['id']}, got {actual.get('id')}."
        assert actual.get("reversed") == expected["reversed"], f"Expected reversed payload '{expected['reversed']}', got '{actual.get('reversed')}'."
        assert actual.get("checksum") == expected["checksum"], f"Expected checksum {expected['checksum']} for '{expected['reversed']}', got {actual.get('checksum')}."