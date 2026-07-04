# test_final_state.py

import os
import subprocess
import time
import pytest

def get_expected_output():
    """
    Derive the expected output by computing the Fibonacci matrix 
    [[1, 1], [1, 0]] to the power of 1048576 modulo 9973.
    """
    def mat_mult(A, B, mod):
        return [
            (A[0]*B[0] + A[1]*B[2]) % mod,
            (A[0]*B[1] + A[1]*B[3]) % mod,
            (A[2]*B[0] + A[3]*B[2]) % mod,
            (A[2]*B[1] + A[3]*B[3]) % mod,
        ]

    def mat_pow(A, p, mod):
        res = [1, 0, 0, 1]
        base = A[:]
        while p > 0:
            if p % 2 == 1:
                res = mat_mult(res, base, mod)
            base = mat_mult(base, base, mod)
            p //= 2
        return res

    res = mat_pow([1, 1, 1, 0], 1048576, 9973)
    return f"Result: [{res[0]}, {res[1]}, {res[2]}, {res[3]}]"

def test_executable_exists():
    agent_bin = "/home/user/project/target/release/matrix_solver"
    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}. Did you build in release mode?"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable."

def test_speedup_and_output():
    agent_bin = "/home/user/project/target/release/matrix_solver"
    ref_bin = "/app/reference_c_impl"

    assert os.path.isfile(ref_bin), "Reference binary missing at /app/reference_c_impl"

    # Run reference implementation
    start_ref = time.perf_counter()
    ref_proc = subprocess.run([ref_bin], capture_output=True, text=True)
    end_ref = time.perf_counter()
    ref_duration = end_ref - start_ref

    # Run agent implementation
    start_agent = time.perf_counter()
    agent_proc = subprocess.run([agent_bin], capture_output=True, text=True)
    end_agent = time.perf_counter()
    agent_duration = end_agent - start_agent

    assert agent_proc.returncode == 0, f"Agent binary failed with exit code {agent_proc.returncode}. stderr: {agent_proc.stderr}"

    # Validate output
    expected_output = get_expected_output()
    actual_output = agent_proc.stdout.strip()
    assert expected_output in actual_output, f"Agent output did not match expected mathematical result.\nExpected to contain: {expected_output}\nGot: {actual_output}"

    # Validate speedup metric
    speedup = ref_duration / agent_duration if agent_duration > 0 else float('inf')
    threshold = 20.0

    assert speedup >= threshold, (
        f"Performance speedup threshold not met.\n"
        f"Measured Speedup: {speedup:.2f}x (Threshold: {threshold}x)\n"
        f"Reference Duration: {ref_duration:.4f}s\n"
        f"Agent Duration: {agent_duration:.4f}s\n"
        f"Ensure you implemented O(log N) binary exponentiation correctly in Rust."
    )