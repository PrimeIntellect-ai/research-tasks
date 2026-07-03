# test_final_state.py

import os
import json
import math
import stat
import subprocess
import pytest

def compute_expected(fasta_content):
    sequences = {}
    current_id = None
    for line in fasta_content.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('>'):
            current_id = line[1:].strip()
            sequences[current_id] = ""
        elif current_id:
            sequences[current_id] += line

    result = {}
    for seq_id, seq in sequences.items():
        raw = []
        for i, char in enumerate(seq):
            raw.append((ord(char) * 10) + (math.sin(i) * 5.0))

        filtered = []
        n = len(raw)
        for i in range(n):
            val_prev = raw[i-1] if i - 1 >= 0 else 0.0
            val_curr = raw[i]
            val_next = raw[i+1] if i + 1 < n else 0.0
            filtered.append(round((val_prev + val_curr + val_next) / 3.0, 2))
        result[seq_id] = filtered
    return result

def test_ml_env_directory_exists():
    path = "/home/user/ml_env"
    assert os.path.isdir(path), f"Environment directory {path} does not exist. You must create it."

def test_training_data_json():
    input_fasta_path = "/home/user/data/input.fasta"
    output_json_path = "/home/user/output/training_data.json"

    assert os.path.isfile(input_fasta_path), f"Input FASTA {input_fasta_path} is missing."
    assert os.path.isfile(output_json_path), f"Output JSON {output_json_path} was not created."

    with open(input_fasta_path, 'r') as f:
        fasta_content = f.read()

    expected_data = compute_expected(fasta_content)

    try:
        with open(output_json_path, 'r') as f:
            actual_data = json.load(f)
    except Exception as e:
        pytest.fail(f"Could not parse {output_json_path} as JSON: {e}")

    for key, expected_arr in expected_data.items():
        assert key in actual_data, f"Sequence ID '{key}' missing in output JSON."
        actual_arr = actual_data[key]
        assert len(expected_arr) == len(actual_arr), f"Length mismatch for sequence '{key}'. Expected {len(expected_arr)}, got {len(actual_arr)}."

        for i, (exp_val, act_val) in enumerate(zip(expected_arr, actual_arr)):
            assert math.isclose(exp_val, act_val, abs_tol=0.01), \
                f"Value mismatch in sequence '{key}' at index {i}: expected {exp_val}, got {act_val}."

def test_test_pipeline_script():
    script_path = "/home/user/test_pipeline.sh"
    assert os.path.isfile(script_path), f"Regression test script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    # Run the script
    try:
        result = subprocess.run([script_path], capture_output=True, text=True, timeout=30)
    except Exception as e:
        pytest.fail(f"Failed to execute {script_path}: {e}")

    assert result.returncode == 0, f"Regression test script failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"