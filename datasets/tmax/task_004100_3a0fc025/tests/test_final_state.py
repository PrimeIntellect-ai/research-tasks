# test_final_state.py

import os
import json
import subprocess
import pytest

def get_expected_variance(input_file):
    count = 0
    mean = 0.0
    m2 = 0.0

    with open(input_file, 'r') as f:
        for line in f:
            val = float(line.strip())
            count += 1
            delta = val - mean
            mean += delta / count
            delta2 = val - mean
            m2 += delta * delta2

    if count < 2:
        return 0.0
    return m2 / count

def test_recovered_threshold():
    recovered_file = '/home/user/recovered_threshold.txt'
    assert os.path.isfile(recovered_file), f"Missing {recovered_file}"
    with open(recovered_file, 'r') as f:
        content = f.read().strip()
    assert content == "42.751", f"Expected threshold to be '42.751', got '{content}'"

def test_requirements_resolved():
    req_file = '/home/user/service/requirements.txt'
    assert os.path.isfile(req_file), f"Missing {req_file}"

    # Check if pip install succeeds (we can use pip install --dry-run if available, 
    # but since it's an isolated environment, just running pip install is fine, 
    # or checking it via subprocess)
    try:
        subprocess.check_call(
            ['pip', 'install', '-r', req_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        pytest.fail("pip install -r requirements.txt failed. Dependency conflict not resolved.")

def test_analyzer_memory_leak_fixed():
    analyzer_file = '/home/user/service/analyzer.py'
    assert os.path.isfile(analyzer_file), f"Missing {analyzer_file}"
    with open(analyzer_file, 'r') as f:
        content = f.read()

    assert "self.history.append" not in content, "analyzer.py still contains 'self.history.append', memory leak not fixed."
    assert "self.history = []" not in content or "self.history" not in content.replace("self.history = []", ""), "analyzer.py still seems to use 'self.history' list."

def test_resolution_json():
    json_file = '/home/user/resolution.json'
    assert os.path.isfile(json_file), f"Missing {json_file}"

    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_file} is not valid JSON")

    assert "recovered_threshold" in data, "Missing 'recovered_threshold' in resolution.json"
    assert "final_variance" in data, "Missing 'final_variance' in resolution.json"

    assert float(data["recovered_threshold"]) == 42.751, "Incorrect recovered_threshold in resolution.json"

    input_file = '/home/user/service/input_data.csv'
    assert os.path.isfile(input_file), f"Missing {input_file}"

    expected_variance = get_expected_variance(input_file)
    actual_variance = float(data["final_variance"])

    assert abs(expected_variance - actual_variance) < 1e-4, f"Expected final_variance ~{expected_variance}, got {actual_variance}"

def test_output_fixed_csv():
    output_file = '/home/user/service/output_fixed.csv'
    assert os.path.isfile(output_file), f"Missing {output_file}"

    with open(output_file, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 100000, f"Expected 100000 lines in {output_file}, got {len(lines)}"

    input_file = '/home/user/service/input_data.csv'
    expected_variance = get_expected_variance(input_file)

    last_val = float(lines[-1])
    assert abs(expected_variance - last_val) < 1e-4, f"Expected last line of output_fixed.csv to be ~{expected_variance}, got {last_val}"