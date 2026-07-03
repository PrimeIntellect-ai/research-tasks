# test_final_state.py

import os
import requests
import pytest

def compute_expected(source: int, dest: int) -> int:
    val = (source ^ dest) + (source * 31) - (dest * 7)
    return val & 0xFFFFFFFF

def test_bench_file_exists():
    bench_file = "/home/user/bench.txt"
    assert os.path.exists(bench_file), f"{bench_file} does not exist. Did you run the benchmark?"
    assert os.path.isfile(bench_file), f"{bench_file} is not a file."

    with open(bench_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().lower()

    assert "requests" in content or "latency" in content or "req/sec" in content, \
        f"{bench_file} does not appear to contain valid benchmark output from ab or wrk."

def test_http_route_endpoint():
    url = "http://127.0.0.1:9000/route"

    test_cases = [
        (100, 200),
        (12345, 67890),
        (0, 0),
        (4294967295, 4294967295)
    ]

    for source, dest in test_cases:
        payload = {"source": source, "destination": dest}
        try:
            response = requests.post(url, json=payload, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to {url} or request timed out: {e}")

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code} for {payload}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {response.text}")

        assert "next_hop" in data, f"Response JSON missing 'next_hop' key: {data}"

        expected_hop = compute_expected(source, dest)
        assert data["next_hop"] == expected_hop, \
            f"Expected next_hop {expected_hop} for source={source}, dest={dest}, but got {data['next_hop']}"