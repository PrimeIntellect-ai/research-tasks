# test_final_state.py
import os
import json
import time
import subprocess
import pytest

def test_run_audit_sh_exists():
    assert os.path.isfile("/home/user/run_audit.sh"), "/home/user/run_audit.sh does not exist."
    assert os.access("/home/user/run_audit.sh", os.X_OK) or os.access("/home/user/run_audit.sh", os.R_OK), "/home/user/run_audit.sh is not readable/executable."

def test_script_execution_and_output():
    script_path = "/home/user/run_audit.sh"

    # Measure execution time
    start = time.time()
    result = subprocess.run(['bash', script_path, '8041'], capture_output=True, text=True)
    end = time.time()

    execution_time = end - start

    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    try:
        output_data = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        pytest.fail(f"Script output is not valid JSON. Output: {result.stdout}")

    assert isinstance(output_data, list), "Output JSON must be a list."
    assert len(output_data) > 0, "Output JSON list is empty."

    first_item = output_data[0]
    assert "path_length" in first_item, "Key 'path_length' missing from output."
    assert "total_duration" in first_item, "Key 'total_duration' missing from output."
    assert "system_chain" in first_item, "Key 'system_chain' missing from output."

    assert isinstance(first_item["system_chain"], list), "'system_chain' must be a list of hostnames."
    assert len(first_item["system_chain"]) > 0, "'system_chain' list is empty."
    assert first_item["system_chain"][0] == "entry.corp.local", "The system chain must start with 'entry.corp.local'."

    assert first_item["path_length"] == 4, f"Expected shortest path length 4, got {first_item['path_length']}."

    assert execution_time < 0.5, f"Execution time {execution_time:.3f}s exceeded the 0.5s threshold."