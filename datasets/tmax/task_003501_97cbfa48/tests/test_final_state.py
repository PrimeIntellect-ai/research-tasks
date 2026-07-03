# test_final_state.py
import re
import subprocess
import pytest

def test_throughput_and_success():
    cmd = ["python3", "/home/user/app/tester/benchmark.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, (
        f"Benchmark script failed with return code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )

    match = re.search(r"Throughput:\s*([\d\.]+)\s*req/s", result.stdout, re.IGNORECASE)
    assert match is not None, (
        f"Could not find 'Throughput: <value> req/s' in benchmark output.\n"
        f"STDOUT:\n{result.stdout}"
    )

    throughput = float(match.group(1))
    assert throughput >= 500.0, f"Throughput was {throughput} req/s, expected >= 500.0 req/s"

    success_match = re.search(r"Success rate:\s*([\d\.]+)%", result.stdout, re.IGNORECASE)
    if success_match:
        success_rate = float(success_match.group(1))
        assert success_rate == 100.0, f"Success rate was {success_rate}%, expected 100.0%"