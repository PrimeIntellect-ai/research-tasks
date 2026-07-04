# test_final_state.py

import os
import json
import subprocess
import pytest

def test_benchmark_result_json():
    json_path = "/home/user/benchmark_result.json"
    assert os.path.isfile(json_path), f"Expected JSON file not found at {json_path}."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "success_count" in data, "JSON missing 'success_count' key."
    assert "time_taken_ms" in data, "JSON missing 'time_taken_ms' key."

    assert data["success_count"] == 10, f"Expected success_count to be 10, got {data['success_count']}."

    time_taken = data["time_taken_ms"]
    assert isinstance(time_taken, (float, int)), f"Expected time_taken_ms to be a number, got {type(time_taken)}."
    assert time_taken > 0, f"Expected time_taken_ms to be strictly greater than 0, got {time_taken}."

def test_shared_library_exists():
    so_path = "/home/user/rust_rate_limiter/target/release/librust_rate_limiter.so"
    assert os.path.isfile(so_path), f"Compiled shared library not found at {so_path}. Did you compile in release mode?"

def test_symbol_exported():
    so_path = "/home/user/rust_rate_limiter/target/release/librust_rate_limiter.so"
    assert os.path.isfile(so_path), "Shared library missing, cannot check symbols."

    # Use nm to check if check_rate_limit is exported and un-mangled.
    # -D checks dynamic symbols.
    result = subprocess.run(["nm", "-D", so_path], capture_output=True, text=True)

    if result.returncode != 0:
        # Fallback to standard nm if -D fails or is unsupported
        result = subprocess.run(["nm", so_path], capture_output=True, text=True)

    output = result.stdout

    # We are looking for the exact un-mangled symbol 'check_rate_limit'
    # Typically it appears as 'T check_rate_limit'
    found = False
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[2] == "check_rate_limit":
            found = True
            break
        elif len(parts) >= 2 and parts[1] == "check_rate_limit":
            found = True
            break

    assert found, "Symbol 'check_rate_limit' not found in the shared library. Ensure #[no_mangle] and extern \"C\" are used."