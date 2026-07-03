# test_final_state.py

import os
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Deploy script at {script_path} is not executable"

def test_benchmark_success_rate():
    bench_path = "/home/user/bench.py"
    assert os.path.isfile(bench_path), f"Benchmark script missing at {bench_path}"

    # Run the benchmark script to get the metric
    result = subprocess.run(
        ["python3", bench_path],
        capture_output=True,
        text=True,
        check=False
    )

    assert result.returncode == 0, f"Benchmark script failed to run. Stderr: {result.stderr}"

    output = result.stdout.strip()
    try:
        # The script prints a single float representing the success rate
        success_rate = float(output.splitlines()[-1])
    except (ValueError, IndexError):
        pytest.fail(f"Benchmark script did not output a valid float. Output: {output}")

    threshold = 0.95
    assert success_rate >= threshold, f"Success rate {success_rate} is below the required threshold of {threshold}"