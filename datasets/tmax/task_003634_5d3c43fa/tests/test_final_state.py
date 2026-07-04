# test_final_state.py
import subprocess
import json
import os
import time

def test_system_throughput():
    """
    Verifies that the system can handle the load test without deadlocking
    and achieves the target throughput threshold.
    """
    load_test_path = "/app/tests/load_test.py"
    assert os.path.isfile(load_test_path), f"Load test script not found at {load_test_path}"

    # Helper to run the load test
    def run_load_test():
        try:
            return subprocess.run(
                ["python3", load_test_path],
                capture_output=True,
                text=True,
                timeout=45  # Should finish well within this if throughput >= 800
            )
        except subprocess.TimeoutExpired:
            return None

    result = run_load_test()

    # If the load test failed (e.g., connection refused), the user might not have left the services running.
    # We will attempt to start them using their script.
    if result is None or result.returncode != 0:
        start_script = "/app/start_services.sh"
        if os.path.isfile(start_script):
            os.chmod(start_script, 0o755)
            # Start services in the background
            subprocess.Popen([start_script], cwd="/app", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(5)  # Give services time to boot

            # Retry load test
            result = run_load_test()

    assert result is not None, "Load test timed out, indicating a deadlock in the worker or API."
    assert result.returncode == 0, f"Load test failed to execute properly.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Parse the JSON output from the load test
    lines = result.stdout.strip().split('\n')
    last_line = lines[-1] if lines else ""

    try:
        data = json.loads(last_line)
    except json.JSONDecodeError:
        assert False, f"Could not parse JSON from load test output. Last line was: {last_line}"

    assert "throughput" in data, f"Missing 'throughput' in load test output: {data}"
    assert "successful" in data, f"Missing 'successful' in load test output: {data}"

    throughput = float(data["throughput"])
    successful = int(data["successful"])

    # Assert correctness
    assert successful == 5000, f"Expected 5000 successful bookings, but got {successful}. The system might still be dropping connections or failing."

    # Assert metric threshold
    assert throughput >= 800.0, f"Throughput of {throughput:.2f} req/sec is below the required threshold of 800.0 req/sec."