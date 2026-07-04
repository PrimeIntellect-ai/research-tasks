# test_final_state.py
import os
import subprocess
import pytest

def test_addon_compiled():
    addon_path = "/app/api-gateway-core/build/Release/validator.node"
    assert os.path.isfile(addon_path), f"Compiled addon not found at {addon_path}. The build configuration may still be broken or 'npm run build' was not executed."

def test_benchmark_results_file_exists():
    assert os.path.isfile("/app/benchmark_results.txt"), "/app/benchmark_results.txt is missing. Did you forget to save the benchmark output?"

def test_addon_performance():
    addon_path = "/app/api-gateway-core/build/Release/validator.node"
    if not os.path.isfile(addon_path):
        pytest.fail("Cannot run performance test because the addon is not compiled.")

    test_script = """
    const addon = require('/app/api-gateway-core/build/Release/validator.node');
    const payload = "A".repeat(100000); // 100KB valid Base64 string

    const start = process.hrtime.bigint();
    for(let i=0; i<1000; i++) {
        const res = addon.validatePayload(payload);
        if (!res) throw new Error("Validation incorrectly failed");
    }
    const end = process.hrtime.bigint();
    const elapsedSec = Number(end - start) / 1e9;
    console.log(elapsedSec);
    """

    try:
        result = subprocess.run(
            ["node", "-e", test_script],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Addon execution failed or validation logic is incorrect. Error: {e.stderr}")

    try:
        time_taken = float(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Could not parse execution time from output: {result.stdout}")

    threshold = 0.25
    assert time_taken <= threshold, f"Performance threshold not met. Time taken: {time_taken}s (Threshold: {threshold}s). The C++ validation logic is still too slow."