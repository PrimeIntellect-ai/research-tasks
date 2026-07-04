# test_final_state.py
import os
import json
import base64
import pytest

def test_source_and_makefile_exist():
    """Verify that the C++ source file and Makefile exist."""
    assert os.path.isfile("/home/user/api_tester.cpp"), "Missing /home/user/api_tester.cpp"
    assert os.path.isfile("/home/user/Makefile"), "Missing /home/user/Makefile"

def test_executable_exists():
    """Verify that the executable was built."""
    assert os.path.isfile("/home/user/api_tester"), "Missing executable /home/user/api_tester"
    assert os.access("/home/user/api_tester", os.X_OK), "/home/user/api_tester is not executable"

def test_output_jsonl_correctness():
    """Verify the output.jsonl matches the expected logic."""
    input_file = "/home/user/requests.json"
    output_file = "/home/user/output.jsonl"

    assert os.path.isfile(input_file), f"Input file missing: {input_file}"
    assert os.path.isfile(output_file), f"Output file missing: {output_file}"

    with open(input_file, "r") as f:
        requests = json.load(f)

    # Recompute expected state
    expected_results = []
    user_history = {}

    for req in requests:
        req_id = req["req_id"]
        user_id = req["user_id"]
        ts = req["timestamp"]
        payload_b64 = req["payload"]

        if user_id not in user_history:
            user_history[user_id] = []

        # Filter history to the rolling 10-second window [ts - 10, ts]
        user_history[user_id] = [t for t in user_history[user_id] if t >= ts - 10]

        if len(user_history[user_id]) < 2:
            # ACCEPTED
            user_history[user_id].append(ts)

            # Transform payload
            decoded = base64.b64decode(payload_b64)
            transformed = bytes(b ^ 0x42 for b in decoded)
            hex_payload = transformed.hex()

            expected_results.append({
                "req_id": req_id,
                "status": "ACCEPTED",
                "processed_payload": hex_payload
            })
        else:
            # RATE_LIMITED
            expected_results.append({
                "req_id": req_id,
                "status": "RATE_LIMITED"
            })

    # Read actual output
    actual_results = []
    with open(output_file, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                actual_results.append(obj)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON on line {line_num} of {output_file}: {line}")

    # Compare
    assert len(actual_results) == len(expected_results), (
        f"Expected {len(expected_results)} output lines, got {len(actual_results)}"
    )

    for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
        assert actual == expected, (
            f"Mismatch at output line {i + 1}.\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )