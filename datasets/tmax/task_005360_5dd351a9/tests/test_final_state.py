# test_final_state.py
import os
import json
import time
import subprocess
import pytest

def run_script(script_path, arg):
    start = time.time()
    result = subprocess.run(["python3", script_path, arg], capture_output=True)
    assert result.returncode == 0, f"Script {script_path} failed with error: {result.stderr.decode()}"
    return time.time() - start

def test_fast_traversal_exists():
    assert os.path.isfile("/home/user/fast_traversal.py"), "Missing /home/user/fast_traversal.py"

def test_speedup_and_correctness():
    slow_script = "/home/user/slow_traversal.py"
    fast_script = "/home/user/fast_traversal.py"
    arg = "SRV-EDGE-42"

    assert os.path.isfile(slow_script), f"Missing {slow_script}"
    assert os.path.isfile(fast_script), f"Missing {fast_script}"

    # Run slow script
    slow_time = run_script(slow_script, arg)

    # Read slow script result if it generates one, or just proceed to run fast script
    # The prompt indicates we should run both and then check path_result.json

    # Run fast script
    fast_time = run_script(fast_script, arg)

    # Calculate speedup
    speedup = slow_time / fast_time if fast_time > 0 else float('inf')

    # Check correctness
    result_file = "/home/user/path_result.json"
    assert os.path.isfile(result_file), f"Missing {result_file}"

    with open(result_file, "r") as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_file} is not valid JSON")

    assert "start_node" in res, "Missing 'start_node' in result"
    assert res["start_node"] == arg, f"Expected start_node '{arg}', got '{res['start_node']}'"
    assert "path" in res, "Missing 'path' in result"
    assert "total_latency" in res, "Missing 'total_latency' in result"

    # Assert speedup threshold
    assert speedup >= 50.0, f"Speedup {speedup:.2f}x is less than required 50.0x (Slow: {slow_time:.4f}s, Fast: {fast_time:.4f}s)"