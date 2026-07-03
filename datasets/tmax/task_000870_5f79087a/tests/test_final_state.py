# test_final_state.py
import subprocess
import re
import pytest

def test_proxy_metric_threshold():
    """
    Runs the verifier script /app/verify.py and asserts that the final score
    meets the threshold of >= 0.95.
    """
    cmd = ["python3", "/app/verify.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"verify.py execution failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    output = result.stdout.strip()

    # Extract floating point numbers from the output (e.g., 0.95, 1.0)
    matches = re.findall(r"0\.\d+|1\.0|\d+\.\d+", output)
    assert matches, f"Could not find a numeric score in verify.py output.\nOutput was:\n{output}"

    # The final score is typically the last number printed
    score = float(matches[-1])

    assert score >= 0.95, f"Metric score {score} is below the required threshold of 0.95.\nOutput was:\n{output}"