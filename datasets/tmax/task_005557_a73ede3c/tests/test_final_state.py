# test_final_state.py
import os
import json
import subprocess
import tempfile

def test_extract_sh_exists_and_executable():
    script_path = '/home/user/extract.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_validate_sh_exists_and_executable():
    script_path = '/home/user/validate.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_extract_produces_correct_json():
    script_path = '/home/user/extract.sh'
    out_file = '/home/user/org_chart.json'

    # Remove out_file if it exists from manual runs
    if os.path.exists(out_file):
        os.remove(out_file)

    # Run extract script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"extract.sh failed with return code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(out_file), f"extract.sh did not create {out_file}."

    with open(out_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{out_file} does not contain valid JSON."

    assert isinstance(data, list), f"JSON root must be an array, got {type(data)}."

    expected_data = [
        {"emp_id": 1, "name": "Alice", "manager_id": None, "depth": 0, "path": "Alice"},
        {"emp_id": 2, "name": "Bob", "manager_id": 1, "depth": 1, "path": "Alice -> Bob"},
        {"emp_id": 3, "name": "Charlie", "manager_id": 2, "depth": 2, "path": "Alice -> Bob -> Charlie"},
        {"emp_id": 4, "name": "David", "manager_id": 3, "depth": 3, "path": "Alice -> Bob -> Charlie -> David"},
        {"emp_id": 5, "name": "Eve", "manager_id": 4, "depth": 4, "path": "Alice -> Bob -> Charlie -> David -> Eve"}
    ]

    # Sort both just in case
    data_sorted = sorted(data, key=lambda x: x.get('emp_id', 0))

    assert len(data_sorted) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data_sorted)}."

    for actual, expected in zip(data_sorted, expected_data):
        assert actual == expected, f"Record mismatch.\nExpected: {expected}\nActual: {actual}"

def test_validate_sh_valid_json():
    script_path = '/home/user/validate.sh'
    out_file = '/home/user/org_chart.json'

    # Assuming extract was successful and created out_file
    if not os.path.exists(out_file):
        subprocess.run(['/home/user/extract.sh'], capture_output=True)

    result = subprocess.run([script_path, out_file], capture_output=True, text=True)
    assert result.returncode == 0, f"validate.sh failed on valid JSON with return code {result.returncode}\nStderr: {result.stderr}"

def test_validate_sh_invalid_json():
    script_path = '/home/user/validate.sh'

    bad_json_1 = '[{"emp_id": 1, "name": "A"}]'
    bad_json_2 = '{"emp_id": 1, "name": "A", "manager_id": null, "depth": 0, "path": "A"}'
    bad_json_3 = '[{"emp_id": 1, "name": "A", "manager_id": null, "depth": "zero", "path": "A"}]'

    for i, bad_content in enumerate([bad_json_1, bad_json_2, bad_json_3]):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(bad_content)
            temp_name = f.name

        try:
            result = subprocess.run([script_path, temp_name], capture_output=True, text=True)
            assert result.returncode == 1, f"validate.sh should fail on bad JSON {i+1} with return code 1, but got {result.returncode}"
        finally:
            os.remove(temp_name)