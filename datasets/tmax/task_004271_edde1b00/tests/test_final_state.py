# test_final_state.py
import os
import subprocess
import time

def test_executable_exists():
    assert os.path.isfile('/app/processor/processor'), "The compiled executable /app/processor/processor is missing. Did you compile the application?"
    assert os.access('/app/processor/processor', os.X_OK), "The file /app/processor/processor is not executable."

def test_execution_time_and_result():
    # Remove result.txt if it exists to ensure we are testing the current run
    if os.path.exists('/app/result.txt'):
        os.remove('/app/result.txt')

    start_time = time.time()
    try:
        result = subprocess.run(
            ['/app/processor/processor', '/app/telemetry.wav'],
            cwd='/app/processor',
            capture_output=True,
            text=True,
            timeout=5.0
        )
    except subprocess.TimeoutExpired:
        assert False, "Execution timed out after 5 seconds. The file reading loop is likely still too slow."

    end_time = time.time()
    execution_time = end_time - start_time

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert os.path.isfile('/app/result.txt'), "The output file /app/result.txt was not created."

    with open('/app/result.txt', 'r') as f:
        output = f.read().strip()

    assert output == "EVT-9942", f"Incorrect result in /app/result.txt. Expected 'EVT-9942', got '{output}'"
    assert execution_time <= 0.5, f"Execution took {execution_time:.3f} seconds, threshold is 0.5 seconds. Optimize the file reading mechanism."