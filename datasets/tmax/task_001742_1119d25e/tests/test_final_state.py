# test_final_state.py

import json
import os
import pytest

def is_prime(n):
    if n < 2: 
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: 
            return False
    return True

def test_qa_report_exists():
    """Check that the qa_report.json file was created."""
    assert os.path.exists('/home/user/qa_report.json'), "The file /home/user/qa_report.json does not exist."
    assert os.path.isfile('/home/user/qa_report.json'), "/home/user/qa_report.json is not a file."

def test_qa_report_content():
    """Check the content of qa_report.json against expected values derived from test_data.txt."""
    data_file = '/home/user/test_data.txt'
    assert os.path.exists(data_file), f"{data_file} is missing."

    with open(data_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    primes = []
    for line in lines:
        val = eval(line)
        if is_prime(val):
            primes.append(val)

    primes.sort(reverse=True)
    expected_prime_count = len(primes)
    expected_top_5 = primes[:5]

    with open('/home/user/qa_report.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/qa_report.json does not contain valid JSON.")

    assert 'peak_memory_bytes' in data, "Missing 'peak_memory_bytes' in qa_report.json"
    assert isinstance(data['peak_memory_bytes'], int), "'peak_memory_bytes' must be an integer"
    assert data['peak_memory_bytes'] > 0, "'peak_memory_bytes' should be a positive integer"

    assert 'prime_count' in data, "Missing 'prime_count' in qa_report.json"
    assert data['prime_count'] == expected_prime_count, f"Expected prime_count {expected_prime_count}, got {data['prime_count']}"

    assert 'top_5_primes' in data, "Missing 'top_5_primes' in qa_report.json"
    assert data['top_5_primes'] == expected_top_5, f"Expected top_5_primes {expected_top_5}, got {data['top_5_primes']}"