# test_final_state.py

import os
import subprocess
import math

def test_statstool_exists():
    assert os.path.isfile("/home/user/workspace/statstool/main.go"), "statstool main.go is missing"
    assert os.path.isfile("/home/user/workspace/statstool/go.mod"), "statstool go.mod is missing"

def test_telemparser_tests_pass():
    """Ensure the user wrote and passes the regression test in telemparser."""
    assert os.path.isfile("/app/telemparser/parser_test.go"), "parser_test.go is missing in /app/telemparser"
    result = subprocess.run(
        ["go", "test", "./..."], 
        cwd="/app/telemparser", 
        capture_output=True, 
        text=True
    )
    assert result.returncode == 0, f"go test failed in /app/telemparser:\n{result.stdout}\n{result.stderr}"

def test_statstool_correct_mean():
    """Compile statstool and verify it computes the correct mean on the evaluation dataset."""
    compile_res = subprocess.run(
        ["go", "build", "-o", "statstool"], 
        cwd="/home/user/workspace/statstool", 
        capture_output=True, 
        text=True
    )
    assert compile_res.returncode == 0, f"Failed to compile statstool:\n{compile_res.stderr}\n{compile_res.stdout}"

    TEST_FILE = "/testdata/eval.bin.enc"
    SECRET_KEY = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
    TRUE_MEAN = 14502394.25

    run_res = subprocess.run(
        ["./statstool", TEST_FILE, SECRET_KEY], 
        cwd="/home/user/workspace/statstool", 
        capture_output=True, 
        text=True
    )
    assert run_res.returncode == 0, f"statstool execution failed:\n{run_res.stderr}\n{run_res.stdout}"

    output = run_res.stdout.strip()
    try:
        agent_mean = float(output)
    except ValueError:
        raise AssertionError(f"statstool output is not a valid float: {output}")

    error = abs(agent_mean - TRUE_MEAN)
    assert error <= 0.001, f"Error {error} exceeds threshold 0.001 (Got {agent_mean}, expected {TRUE_MEAN})"