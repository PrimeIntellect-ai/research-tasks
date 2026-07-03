# test_final_state.py

import os
import subprocess
import time
import random
import string
import pytest

def test_encoder_compiled_and_executable():
    path = "/home/user/src/encoder"
    assert os.path.isfile(path), f"Compiled encoder binary not found at {path}"
    assert os.access(path, os.X_OK), f"Compiled encoder binary at {path} is not executable"

def test_benchmark_script_exists_and_executable():
    path = "/home/user/benchmark.sh"
    assert os.path.isfile(path), f"Benchmark script not found at {path}"
    assert os.access(path, os.X_OK), f"Benchmark script at {path} is not executable"

def test_report_log_exists():
    path = "/home/user/report.log"
    assert os.path.isfile(path), f"Report log not found at {path}"

def test_encoder_correctness():
    """Verify that the compiled encoder produces the exact same output as the oracle."""
    encoder_path = "/home/user/src/encoder"
    oracle_path = "/app/oracle_bin"

    for _ in range(10):
        length = random.randint(10, 1000)
        test_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode()

        try:
            res_encoder = subprocess.run([encoder_path], input=test_str, capture_output=True, check=True, timeout=2)
            res_oracle = subprocess.run([oracle_path], input=test_str, capture_output=True, check=True, timeout=2)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Execution failed for string of length {length}. Return code: {e.returncode}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Execution timed out for string of length {length}")

        assert res_encoder.stdout == res_oracle.stdout, f"Output mismatch for input length {length}"

def test_speedup_metric():
    """Verify the accuracy of the calculated execution speedup ratio."""
    report_path = "/home/user/report.log"

    try:
        with open(report_path, 'r') as f:
            content = f.read().strip()
            agent_speedup = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {report_path} as a float: '{content}'")

    encoder_path = "/home/user/src/encoder"
    oracle_path = "/app/oracle_bin"

    c_time = 0
    oracle_time = 0

    for _ in range(100):
        test_str = ''.join(random.choices(string.ascii_letters + string.digits, k=500)).encode()

        t0 = time.time()
        subprocess.run([encoder_path], input=test_str, stdout=subprocess.DEVNULL)
        c_time += time.time() - t0

        t0 = time.time()
        subprocess.run([oracle_path], input=test_str, stdout=subprocess.DEVNULL)
        oracle_time += time.time() - t0

    true_speedup = c_time / oracle_time
    relative_error = abs(agent_speedup - true_speedup) / true_speedup

    assert relative_error <= 0.25, (
        f"Speedup ratio relative error is too high. "
        f"Agent reported: {agent_speedup:.4f}, True speedup: {true_speedup:.4f}, "
        f"Relative error: {relative_error:.4f} (Threshold: <= 0.25)"
    )