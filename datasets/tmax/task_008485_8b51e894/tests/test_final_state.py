# test_final_state.py
import os
import subprocess

def test_test_runner_exists():
    assert os.path.isfile('/home/user/util_dev/test_runner.sh'), "/home/user/util_dev/test_runner.sh does not exist"

def test_test_runner_execution_and_outputs():
    # Run the test runner
    result = subprocess.run(
        ['bash', 'test_runner.sh'],
        cwd='/home/user/util_dev',
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"test_runner.sh failed with exit code {result.returncode}:\n{result.stderr}"

    # Check test_log.txt
    log_path = '/home/user/util_dev/test_log.txt'
    assert os.path.isfile(log_path), f"{log_path} was not generated"
    with open(log_path, 'r') as f:
        lines = f.read().splitlines()
    assert len(lines) >= 8, f"{log_path} has fewer than 8 lines (found {len(lines)})"

    # Check diff_output.txt
    diff_path = '/home/user/util_dev/diff_output.txt'
    assert os.path.isfile(diff_path), f"{diff_path} was not generated"
    assert os.path.getsize(diff_path) == 0, f"{diff_path} is not empty, indicating differences between C and Python outputs"

def test_fast_parser_fixes_lowercase_hex():
    # Create a secret test log to ensure lowercase hex is handled
    # 2f6170692f76312f decodes to /api/v1/
    secret_log = (
        "100 1.1.1.1 2f6170692f76312f\n"
        "101 1.1.1.1 2f6170692f76312f\n"
        "102 1.1.1.1 2f6170692f76312f\n"
    )

    # Run C parser
    c_parser_path = '/home/user/util_dev/fast_parser'
    assert os.path.isfile(c_parser_path), f"Compiled executable {c_parser_path} not found"

    c_result = subprocess.run(
        [c_parser_path],
        input=secret_log,
        text=True,
        capture_output=True
    )
    assert c_result.returncode == 0, "fast_parser execution failed on secret log"

    # Run Python parser
    py_parser_path = '/home/user/util_dev/legacy_parser.py'
    py_result = subprocess.run(
        ['python3', py_parser_path],
        input=secret_log,
        text=True,
        capture_output=True
    )
    assert py_result.returncode == 0, "legacy_parser.py execution failed on secret log"

    # Compare outputs
    c_out = sorted(c_result.stdout.strip().splitlines())
    py_out = sorted(py_result.stdout.strip().splitlines())

    assert c_out == py_out, (
        f"Outputs differ on lowercase hex input.\n"
        f"C output: {c_out}\n"
        f"Python output: {py_out}\n"
        "The C parser likely still fails on lowercase hex decoding."
    )