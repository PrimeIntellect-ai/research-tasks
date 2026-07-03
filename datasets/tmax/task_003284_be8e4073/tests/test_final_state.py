# test_final_state.py

import os
import subprocess
import json

def test_downtime_summary():
    file_path = "/home/user/downtime_summary.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you save the final output?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "105", f"Expected downtime summary to be '105', but got '{content}'."

def test_log_parser_builds_and_runs():
    c_file = "/home/user/uptime/log_parser.c"
    exe_file = "/home/user/uptime/log_parser"

    assert os.path.isfile(c_file), "log_parser.c is missing."

    # Ensure it builds
    build_result = subprocess.run(["make", "-C", "/home/user/uptime"], capture_output=True)
    assert build_result.returncode == 0, f"make failed: {build_result.stderr.decode()}"
    assert os.path.isfile(exe_file), "log_parser executable was not created."

    # Ensure it produces valid JSON
    run_result = subprocess.run([exe_file], input=b"test\n", capture_output=True)
    assert run_result.returncode == 0, "log_parser crashed when running."

    try:
        data = json.loads(run_result.stdout.decode())
        assert isinstance(data, dict), "log_parser output is not a JSON dictionary."
    except json.JSONDecodeError:
        pytest.fail("log_parser did not output valid JSON.")

def test_aggregator_fixed():
    py_file = "/home/user/uptime/aggregator.py"
    assert os.path.isfile(py_file), "aggregator.py is missing."

    # Test aggregator with the expected JSON output
    test_json = '{"region_us": {"east": 45, "west": [10, 5, {"node1": 2}]}, "region_eu": [20, 15], "region_ap": 8}\n'
    run_result = subprocess.run(["python3", py_file], input=test_json.encode(), capture_output=True)

    assert run_result.returncode == 0, f"aggregator.py failed to run: {run_result.stderr.decode()}"
    assert run_result.stdout.decode().strip() == "105", "aggregator.py did not output the correct sum."