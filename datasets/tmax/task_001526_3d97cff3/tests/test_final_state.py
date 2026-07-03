# test_final_state.py

import os
import re
import subprocess
import pytest

def test_vendored_package_fixed():
    version_go_path = "/app/semver/version.go"
    assert os.path.isfile(version_go_path), f"File missing: {version_go_path}"
    with open(version_go_path, "r") as f:
        content = f.read()
    assert "package semver" in content, "The typo 'pacakge semver' was not fixed to 'package semver' in /app/semver/version.go"
    assert "pacakge semver" not in content, "The typo 'pacakge semver' is still present in /app/semver/version.go"

def test_benchmark_performance():
    processor_dir = "/home/user/processor"
    assert os.path.isdir(processor_dir), f"Directory missing: {processor_dir}"

    # Run the benchmark
    try:
        result = subprocess.run(
            ["go", "test", "-bench=BenchmarkFilterVersions", "-benchtime=10000x"],
            cwd=processor_dir,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"go test failed to run or compile. Output:\n{e.stdout}\n{e.stderr}")

    output = result.stdout
    # Look for the benchmark line, e.g.: BenchmarkFilterVersions-8   10000   1500 ns/op
    match = re.search(r'BenchmarkFilterVersions.*?\s+\d+\s+([\d.]+)\s+ns/op', output)
    assert match is not None, f"Could not find ns/op metric in benchmark output:\n{output}"

    ns_op = float(match.group(1))
    threshold = 10000.0
    assert ns_op <= threshold, f"Benchmark execution time {ns_op} ns/op is greater than threshold {threshold} ns/op. Optimization is insufficient."

def test_cross_compiled_binaries():
    amd64_path = "/home/user/processor/build/processor-amd64"
    arm64_path = "/home/user/processor/build/processor-arm64"

    assert os.path.isfile(amd64_path), f"Binary missing: {amd64_path}"
    assert os.path.isfile(arm64_path), f"Binary missing: {arm64_path}"

    # Check architecture using 'file' command
    try:
        amd64_file = subprocess.run(["file", amd64_path], capture_output=True, text=True, check=True).stdout
        arm64_file = subprocess.run(["file", arm64_path], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run 'file' command on binaries. Error:\n{e.stderr}")

    assert "x86-64" in amd64_file, f"Expected x86-64 architecture for {amd64_path}, got: {amd64_file}"
    assert "aarch64" in arm64_file, f"Expected aarch64 architecture for {arm64_path}, got: {arm64_file}"