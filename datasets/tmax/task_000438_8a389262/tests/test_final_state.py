# test_final_state.py
import os
import json
import csv
import stat
import pytest

def test_go_mod_exists():
    go_mod_path = "/home/user/pipeline/go.mod"
    assert os.path.isfile(go_mod_path), f"{go_mod_path} is missing. Did you initialize the go module?"
    with open(go_mod_path, "r") as f:
        content = f.read()
    assert "module data-pipeline" in content, "go.mod does not declare the module 'data-pipeline'"

def test_process_test_go_exists_and_uses_testify():
    test_file_path = "/home/user/pipeline/process_test.go"
    assert os.path.isfile(test_file_path), f"{test_file_path} is missing."
    with open(test_file_path, "r") as f:
        content = f.read()
    assert "github.com/stretchr/testify/assert" in content, "process_test.go does not use github.com/stretchr/testify/assert"
    assert "func TestNormalize" in content or "func Test" in content, "process_test.go does not seem to contain a test function"

def test_run_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."
    with open(script_path, "r") as f:
        content = f.read()
    assert "cd /home/user/pipeline" in content, "Script does not change directory to /home/user/pipeline"
    assert "go test" in content, "Script does not run go test"
    assert "process.go" in content or "go run" in content, "Script does not run process.go"

def test_processed_json_correctness():
    json_path = "/home/user/data/processed.json"
    csv_path = "/home/user/data/raw_measurements.csv"

    assert os.path.isfile(csv_path), "Raw CSV is missing."
    assert os.path.isfile(json_path), f"{json_path} is missing. Did the pipeline run successfully?"

    # Recompute expected values from CSV
    ids = []
    values = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.append(int(row["id"]))
            values.append(float(row["measurement"]))

    min_val = min(values)
    max_val = max(values)

    expected_normalized = []
    for v in values:
        if min_val == max_val:
            expected_normalized.append(0.0)
        else:
            expected_normalized.append((v - min_val) / (max_val - min_val))

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("processed.json is not a valid JSON file.")

    assert isinstance(data, list), "processed.json should contain an array of objects."
    assert len(data) == len(expected_normalized), "Mismatch in number of records in processed.json."

    for i, expected_val in enumerate(expected_normalized):
        record = data[i]
        assert "id" in record, f"Record {i} missing 'id' field."
        assert "value" in record, f"Record {i} missing 'value' field."
        assert record["id"] == ids[i], f"ID mismatch at index {i}: expected {ids[i]}, got {record['id']}"
        assert abs(record["value"] - expected_val) <= 1e-4, f"Value mismatch at index {i}: expected {expected_val}, got {record['value']}"