# test_final_state.py

import os
import subprocess
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_analyze_script_no_python_or_r():
    script_path = "/home/user/analyze.sh"
    with open(script_path, 'r') as f:
        content = f.read().lower()

    assert "python" not in content, "Script must not use Python."
    assert "rscript" not in content, "Script must not use R."

def test_analyze_script_output():
    script_path = "/home/user/analyze.sh"

    # Run the student's script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    # Compute expected output using the exact logic provided in the truth
    truth_script = """
awk -F, '
NR>1 { z[++n] = $1 * $2 }
END {
    srand(123);
    for (i=1; i<=1000; i++) {
        sum = 0;
        for (j=1; j<=n; j++) {
            idx = int(rand() * n) + 1;
            sum += z[idx];
        }
        mean = sum / n;
        printf "%.6f\\n", mean;
    }
}' /home/user/dataset.csv | sort -n > /tmp/means_truth.txt

LOWER=$(head -n 25 /tmp/means_truth.txt | tail -n 1)
UPPER=$(head -n 975 /tmp/means_truth.txt | tail -n 1)
printf "CI: [%.4f, %.4f]\\n" "$LOWER" "$UPPER"
"""
    truth_result = subprocess.run(["bash", "-c", truth_script], capture_output=True, text=True)
    expected_output = truth_result.stdout.strip()

    student_output = result.stdout.strip()
    assert student_output == expected_output, f"Expected output '{expected_output}', but got '{student_output}'"