# test_final_state.py

import os
import json
import subprocess
import pytest

def test_cjson_built():
    so_path = '/app/cJSON-1.7.15/libcjson.so'
    assert os.path.isfile(so_path), f"{so_path} is missing. cJSON was not built correctly."

def test_pipeline_binary_exists():
    bin_path = '/home/user/pipeline/inference_pipeline'
    assert os.path.isfile(bin_path), f"{bin_path} is missing. Pipeline was not compiled."
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

def test_experiment_log_schema():
    log_path = '/home/user/pipeline/experiment_log.json'
    assert os.path.isfile(log_path), f"{log_path} is missing. The pipeline did not generate the log."

    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{log_path} is not a valid JSON file.")

    def check_no_floats(obj):
        if isinstance(obj, float):
            return False
        elif isinstance(obj, dict):
            return all(check_no_floats(v) for v in obj.values())
        elif isinstance(obj, list):
            return all(check_no_floats(v) for v in obj)
        return True

    assert check_no_floats(data), "Schema violation: Found floating-point numbers in experiment_log.json. Expected strictly integers (e.g., missing values as -1)."

def test_inference_speedup():
    # The verifier script /app/verify.py evaluates the speedup and schema.
    # We run it to ensure the metric threshold (speedup >= 2.0) is met.
    verify_path = '/app/verify.py'
    assert os.path.isfile(verify_path), f"{verify_path} is missing."

    result = subprocess.run(['python3', verify_path], capture_output=True, text=True)

    # Check if the verifier script passed, which enforces speedup >= 2.0 internally
    assert result.returncode == 0, f"Verifier failed. Output:\n{result.stdout}\nError:\n{result.stderr}"

    # Attempt to parse speedup from output if available to explicitly assert it
    speedup = None
    for line in result.stdout.splitlines():
        if "speedup" in line.lower():
            try:
                # Naive extraction of the first float found in the line
                words = line.split()
                for w in words:
                    try:
                        val = float(w.strip(','))
                        if val > 0:
                            speedup = val
                            break
                    except ValueError:
                        pass
            except Exception:
                pass

    if speedup is not None:
        assert speedup >= 2.0, f"Speedup is {speedup:.2f}, which is below the threshold of 2.0."