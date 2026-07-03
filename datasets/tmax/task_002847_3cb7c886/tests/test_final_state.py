# test_final_state.py
import time
import subprocess
import json
import os
import pytest

def test_analyze_supply_chain_execution_and_output():
    script_path = "/home/user/analyze_supply_chain.py"
    output_path = "/home/user/output.json"

    assert os.path.exists(script_path), f"Script not found at {script_path}"

    # Remove output.json if it exists to ensure the script generates it fresh
    if os.path.exists(output_path):
        os.remove(output_path)

    start = time.time()
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    duration = time.time() - start

    assert result.returncode == 0, (
        f"Script failed with return code {result.returncode}.\n"
        f"Stdout: {result.stdout}\n"
        f"Stderr: {result.stderr}"
    )

    assert os.path.exists(output_path), f"Output file not found at {output_path}"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse JSON from {output_path}")

    assert "max_depth" in data, "Key 'max_depth' missing in output.json"
    assert "total_nodes" in data, "Key 'total_nodes' missing in output.json"
    assert "total_edges" in data, "Key 'total_edges' missing in output.json"

    assert data["max_depth"] == 14, f"Expected max_depth 14, got {data['max_depth']}"
    assert data["total_nodes"] == 50000, f"Expected 50000 nodes, got {data['total_nodes']}"
    assert data["total_edges"] == 49999, f"Expected 49999 edges, got {data['total_edges']}"

    assert duration <= 3.0, f"Execution time {duration:.2f}s exceeded threshold of 3.0s"