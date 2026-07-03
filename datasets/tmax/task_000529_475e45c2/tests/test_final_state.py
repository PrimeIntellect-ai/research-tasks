# test_final_state.py

import os
import sys
import subprocess
import importlib.util

def test_mre_log_exists_and_minimal():
    """Test that mre_log.txt exists and contains the absolute minimum number of log lines."""
    mre_path = '/home/user/mre_log.txt'
    assert os.path.exists(mre_path), f"File {mre_path} does not exist."

    with open(mre_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, "MRE log must have at least 3 lines to form a cycle and trigger it."
    assert len(lines) <= 4, "MRE log should be minimal (<= 4 lines)."

    requires_count = sum(1 for line in lines if ',REQUIRES,' in line)
    completed_count = sum(1 for line in lines if ',COMPLETED' in line)

    assert requires_count >= 2, "MRE log must contain at least two REQUIRES statements to form a cycle."
    assert completed_count >= 1, "MRE log must contain a COMPLETED statement to trigger the resolution."

def test_log_processor_raises_value_error_on_cycle():
    """Test that the fixed log_processor.py raises ValueError with specific message on cycle."""
    processor_path = '/home/user/log_processor.py'
    assert os.path.exists(processor_path), f"File {processor_path} does not exist."

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location("log_processor", processor_path)
    log_processor = importlib.util.module_from_spec(spec)
    sys.modules["log_processor"] = log_processor
    spec.loader.exec_module(log_processor)

    assert hasattr(log_processor, 'process_logs'), "log_processor.py must have process_logs function."

    mre_lines = [
        "A,REQUIRES,B",
        "B,REQUIRES,A",
        "A,COMPLETED"
    ]

    error_raised = False
    try:
        log_processor.process_logs(mre_lines)
    except ValueError as e:
        error_raised = True
        assert str(e) == "Cycle detected in job dependencies", f"Incorrect ValueError message: {e}"
    except Exception as e:
        assert False, f"Expected ValueError, but got {type(e).__name__}: {e}"

    assert error_raised, "log_processor.py did not raise ValueError on cyclic dependencies."

def test_regression_test_script_success():
    """Test that regression_test.py runs and exits with code 0."""
    regression_test_path = '/home/user/regression_test.py'
    assert os.path.exists(regression_test_path), f"File {regression_test_path} does not exist."

    # Run the regression test script
    try:
        result = subprocess.run(
            [sys.executable, regression_test_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        assert result.returncode == 0, f"regression_test.py exited with code {result.returncode}, expected 0. Output: {result.stdout} {result.stderr}"
    except subprocess.TimeoutExpired:
        assert False, "regression_test.py timed out, indicating the infinite loop might still be present."