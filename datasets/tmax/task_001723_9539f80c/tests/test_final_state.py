# test_final_state.py

import os
import random
import subprocess
import pytest

def test_proxy_check_fuzz_equivalence():
    """Verify that the student's script perfectly matches the oracle's output on random inputs."""
    student_script = "/home/user/proxy_check.py"
    oracle_bin = "/app/oracle_proxy_check"

    assert os.path.exists(student_script), f"Student script missing at {student_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary missing at {oracle_bin}"

    random.seed(42)

    for _ in range(1000):
        # Generate random 16-character hexadecimal string
        hex_input = "".join(random.choices("0123456789abcdef", k=16))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_bin, hex_input],
                capture_output=True,
                text=True,
                timeout=2,
                check=True
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {hex_input} with error: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on input {hex_input}")

        # Run student script
        try:
            student_proc = subprocess.run(
                ["python3", student_script, hex_input],
                capture_output=True,
                text=True,
                timeout=2
            )
            student_out = student_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Student script timed out on input {hex_input}")

        assert student_proc.returncode == 0, (
            f"Student script exited with code {student_proc.returncode} on input {hex_input}.\n"
            f"Stderr: {student_proc.stderr}"
        )

        assert student_out == oracle_out, (
            f"Output mismatch on input {hex_input}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Actual (Student):  {student_out}"
        )