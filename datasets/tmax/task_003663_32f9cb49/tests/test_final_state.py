# test_final_state.py

import os
import json
import re
import pytest

def test_math_ops_patched():
    math_ops_path = "/home/user/rust_proj/src/math_ops.rs"
    assert os.path.isfile(math_ops_path), f"File {math_ops_path} does not exist."

    with open(math_ops_path, "r") as f:
        content = f.read()

    assert "a + b" in content, "math_ops.rs does not contain the fixed 'a + b' logic."
    assert "a * b" in content, "math_ops.rs does not contain the fixed 'a * b' logic."
    assert "BUG" not in content, "math_ops.rs still contains the original buggy comments."
    assert "a - b" not in content, "math_ops.rs still contains the original subtraction bug."
    assert "a / b" not in content, "math_ops.rs still contains the original division bug."

def test_constants_rs_generated():
    constants_path = "/home/user/rust_proj/src/constants.rs"
    assert os.path.isfile(constants_path), f"File {constants_path} does not exist."

    with open(constants_path, "r") as f:
        content = f.read()

    # Check definition format
    assert "pub const PRIMES: [u32; 100] =" in content, "constants.rs does not contain the expected variable definition 'pub const PRIMES: [u32; 100] ='."

    # Extract numbers from the array
    try:
        array_content = content.split("=")[1].strip().strip(";").strip("[]")
        numbers = [int(x.strip()) for x in array_content.split(",") if x.strip()]
    except Exception as e:
        pytest.fail(f"Failed to parse the array of primes in constants.rs: {e}")

    # Generate the first 100 expected primes
    expected_primes = []
    num = 2
    while len(expected_primes) < 100:
        is_prime = True
        for p in expected_primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            expected_primes.append(num)
        num += 1

    assert len(numbers) == 100, f"Expected exactly 100 primes, but found {len(numbers)}."
    assert numbers == expected_primes, "The array in constants.rs does not match the first 100 prime numbers."

def test_benchmark_json_generated():
    bench_path = "/home/user/benchmark.json"
    assert os.path.isfile(bench_path), f"File {bench_path} does not exist."

    with open(bench_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("benchmark.json does not contain valid JSON.")

    expected_keys = ["10", "100", "1000"]
    for key in expected_keys:
        assert key in data, f"Key '{key}' is missing from benchmark.json."
        assert isinstance(data[key], float), f"Value for key '{key}' is not a float (got {type(data[key]).__name__})."
        assert data[key] >= 0.0, f"Value for key '{key}' is negative, which is invalid for execution time."