# test_final_state.py
import os
import json
import time
import subprocess

def compute_sum_of_divisors(n: int) -> int:
    if n == 0:
        return 0
    total = 0
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total

def test_output_correctness():
    assert os.path.isfile("/app/input.json"), "Input file missing"
    assert os.path.isfile("/app/output.json"), "Output file missing"

    with open("/app/input.json", "r") as f:
        inputs = json.load(f)

    with open("/app/output.json", "r") as f:
        outputs = json.load(f)

    for n in inputs:
        expected = compute_sum_of_divisors(n)
        actual = outputs.get(str(n))
        assert actual == expected, f"Incorrect sum of divisors for {n}: expected {expected}, got {actual}"

def test_concurrency_speedup():
    binary_path = "/app/bin/worker"
    assert os.path.isfile(binary_path), "Worker binary missing"

    # Ensure the library path is set
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/app/divsum-0.1.0/target/release:" + env.get("LD_LIBRARY_PATH", "")

    # Measure time with GOMAXPROCS=1 (serial baseline)
    env["GOMAXPROCS"] = "1"
    start_serial = time.time()
    subprocess.run([binary_path], env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    serial_time = time.time() - start_serial

    # Measure time with GOMAXPROCS=4 (concurrent)
    env["GOMAXPROCS"] = "4"
    start_concurrent = time.time()
    subprocess.run([binary_path], env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    concurrent_time = time.time() - start_concurrent

    speedup = serial_time / concurrent_time
    assert speedup >= 2.0, f"Speedup too low: {speedup:.2f} (Serial: {serial_time:.2f}s, Concurrent: {concurrent_time:.2f}s). Expected at least 2.0."