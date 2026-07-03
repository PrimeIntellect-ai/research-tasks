# test_final_state.py

import os
import subprocess
import pytest

def test_latest_logs_symlink():
    """Check that the latest_logs symlink was created and points to the correct directory."""
    symlink_path = "/home/user/app/latest_logs"
    target_path = "/home/user/app/services/logs"

    assert os.path.islink(symlink_path), f"Expected {symlink_path} to be a symbolic link."

    # Resolve the symlink target (handle relative or absolute symlinks)
    actual_target = os.readlink(symlink_path)
    absolute_target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), actual_target))

    assert absolute_target == target_path, f"Symlink {symlink_path} points to {absolute_target}, expected {target_path}."

def test_perturbation_removed():
    """Verify that the artificial delay has been removed from the vendored urllib3 source code."""
    connection_py = "/home/user/app/urllib3-src/src/urllib3/connection.py"
    assert os.path.isfile(connection_py), f"Vendored urllib3 source file missing at {connection_py}."

    with open(connection_py, "r", encoding="utf-8") as f:
        content = f.read()

    assert "time.sleep(0.5)" not in content, "The artificial delay 'time.sleep(0.5)' is still present in connection.py."

def test_performance_metric():
    """Run the verifier benchmark script and assert the runtime is within the acceptable threshold."""
    benchmark_script = "/home/user/verifier_benchmark.py"
    assert os.path.isfile(benchmark_script), f"Benchmark script {benchmark_script} is missing."

    try:
        result = subprocess.run(
            ["python3", benchmark_script],
            capture_output=True,
            text=True,
            check=True,
            timeout=15.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Benchmark script timed out after 15 seconds. The 0.5s delay per request is likely still active.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Benchmark script failed with exit code {e.returncode}. Stderr: {e.stderr}")

    output = result.stdout.strip()
    try:
        runtime = float(output)
    except ValueError:
        pytest.fail(f"Benchmark script returned non-float output: {output}")

    assert runtime <= 1.0, f"Performance metric failed: runtime was {runtime:.3f} seconds, expected <= 1.0 seconds."