# test_final_state.py
import os
import random
import subprocess
import io
import csv
import pytest

def test_script_exists():
    script_path = "/home/user/analyze_jitter.py"
    assert os.path.isfile(script_path), f"Student script {script_path} is missing."

def test_package_installed():
    result = subprocess.run(
        ["python3", "-c", "import fast_stat_profiler"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f"Failed to import fast_stat_profiler. Ensure it is installed system-wide or in the user environment.\n"
        f"Error: {result.stderr}"
    )

def generate_csv():
    num_rows = random.randint(100, 1000)
    out = io.StringIO()
    writer = csv.writer(out)
    for _ in range(num_rows):
        ts = random.randint(1000000, 9999999)
        rand_val = random.random()
        if rand_val < 0.05:
            val = "NaN"
        elif rand_val < 0.15:
            val = -random.random() * 1000.0
        else:
            val = random.random() * 1000.0
        writer.writerow([ts, val])
    return out.getvalue()

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = "/oracle/analyze_jitter_oracle.py"
    student_path = "/home/user/analyze_jitter.py"

    for i in range(100):
        input_data = generate_csv()

        oracle_res = subprocess.run(
            ["python3", oracle_path],
            input=input_data,
            text=True,
            capture_output=True
        )

        student_res = subprocess.run(
            ["python3", student_path],
            input=input_data,
            text=True,
            capture_output=True
        )

        assert student_res.returncode == 0, (
            f"Student script failed on test case {i}.\n"
            f"Stderr:\n{student_res.stderr}\n"
            f"Stdout:\n{student_res.stdout}"
        )
        assert oracle_res.returncode == 0, f"Oracle failed on test case {i}. Stderr: {oracle_res.stderr}"

        assert student_res.stdout == oracle_res.stdout, (
            f"Output mismatch on test case {i}.\n"
            f"Input data (first 200 chars):\n{input_data[:200]}...\n"
            f"Expected Output:\n{oracle_res.stdout}\n"
            f"Actual Output:\n{student_res.stdout}"
        )