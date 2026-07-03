# test_final_state.py

import os
import subprocess
import json
import pytest

def test_answer_txt_exists_and_correct():
    answer_file = "/home/user/answer.txt"
    assert os.path.isfile(answer_file), f"File {answer_file} does not exist."

    with open(answer_file, "r") as f:
        content = f.read().strip()

    assert content == "10173646", f"Expected '10173646' in {answer_file}, but got '{content}'."

def test_benchmark_sh_exists_and_executable():
    script_file = "/home/user/benchmark.sh"
    assert os.path.isfile(script_file), f"File {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"File {script_file} is not executable."

def test_benchmark_result_exists_and_not_empty():
    result_file = "/home/user/benchmark_result.txt"
    assert os.path.isfile(result_file), f"File {result_file} does not exist."
    assert os.path.getsize(result_file) > 0, f"File {result_file} is empty."

def test_grpc_server_running_and_correct():
    cmd = [
        "grpcurl",
        "-plaintext",
        "-d", '{"value": 5}',
        "127.0.0.1:50051",
        "transform_api.TransformService/ApplyTransform"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    except FileNotFoundError:
        pytest.fail("grpcurl command not found.")
    except subprocess.TimeoutExpired:
        pytest.fail("grpcurl command timed out. Is the gRPC server running?")

    assert result.returncode == 0, f"grpcurl failed with error: {result.stderr}"

    try:
        response_json = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse gRPC response as JSON. Output was: {result.stdout}")

    # The result field could be a string or integer depending on protobuf JSON mapping for uint64
    res_val = str(response_json.get("result", ""))
    assert res_val == "11262442", f"Expected result '11262442', but got '{res_val}'."