# test_final_state.py
import os
import json
import subprocess
import pytest

BASE_DIR = "/home/user/data_pipeline"

def test_build_script_executes_successfully():
    build_script = os.path.join(BASE_DIR, "build.sh")
    assert os.path.isfile(build_script), f"File missing: {build_script}"

    # Run the build script to ensure it completes without errors
    result = subprocess.run([build_script], cwd=BASE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"build.sh failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_combined_json_output():
    output_file = os.path.join(BASE_DIR, "output", "combined.json")
    assert os.path.isfile(output_file), f"Output file missing: {output_file}"

    with open(output_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {output_file} as JSON: {e}")

    assert isinstance(data, list), "The combined.json file must contain a JSON array."
    assert len(data) == 3, f"Expected exactly 3 objects in the JSON array, but found {len(data)}."

    found_ids = set()
    for index, item in enumerate(data):
        assert isinstance(item, dict), f"Item at index {index} is not a dictionary."
        assert "auth" in item, f"Item at index {index} is missing the 'auth' key."
        assert item["auth"] == "SUPER_SECRET_99X", f"Item at index {index} has incorrect 'auth' value: {item['auth']}"

        assert "id" in item, f"Item at index {index} is missing the 'id' key."
        found_ids.add(item["id"])

    assert found_ids == {1, 2, 3}, f"Expected IDs 1, 2, and 3 in the combined output, but found {found_ids}."

def test_data_files_untouched():
    data_dir = os.path.join(BASE_DIR, "data")
    expected_files = {"file 1.json", "file 2.json", "file 3 spaces.json"}
    actual_files = set(os.listdir(data_dir))

    assert expected_files.issubset(actual_files), f"Some data files were missing or renamed. Expected at least {expected_files}, found {actual_files}"