# test_final_state.py
import os
import subprocess
import pytest

def test_detector_script_f1_score():
    script_path = "/home/user/detector.py"
    test_log_path = "/hidden/test_log.json"

    assert os.path.isfile(script_path), f"Detector script not found at {script_path}"
    assert os.path.isfile(test_log_path), f"Hidden test log not found at {test_log_path}"

    expected_ids = {"req_102", "req_105", "req_110", "req_111", "req_119", "req_120", "req_135", "req_142"}

    try:
        result = subprocess.run(
            ["python3", script_path, test_log_path],
            capture_output=True,
            text=True,
            timeout=15
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Script {script_path} timed out after 15 seconds.")
    except Exception as e:
        pytest.fail(f"Failed to execute script {script_path}: {e}")

    assert result.returncode == 0, f"Script exited with non-zero status code {result.returncode}.\nStderr: {result.stderr}"

    output_ids = set(line.strip() for line in result.stdout.splitlines() if line.strip())

    tp = len(expected_ids.intersection(output_ids))
    fp = len(output_ids - expected_ids)
    fn = len(expected_ids - output_ids)

    if tp == 0:
        f1 = 0.0
    else:
        f1 = 2 * tp / (2 * tp + fp + fn)

    assert f1 >= 0.95, f"F1 Score {f1:.4f} is below the threshold of 0.95. Expected IDs: {expected_ids}, Output IDs: {output_ids}"