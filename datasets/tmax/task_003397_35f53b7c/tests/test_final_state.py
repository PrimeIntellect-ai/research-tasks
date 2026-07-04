# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    oracle_bin = "/opt/oracle/normalize_oracle"
    student_bin = "/home/user/normalize"

    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.path.isfile(student_bin), f"Student binary not found at {student_bin}"
    assert os.access(student_bin, os.X_OK), f"Student binary {student_bin} is not executable"

    random.seed(42)

    # Generate 1000 test cases to ensure good coverage without timing out
    # We will mix completely random bytes with specific prefixes to hit all branches
    test_cases = []
    for _ in range(1000):
        choice = random.random()
        buf = bytearray(random.getrandbits(8) for _ in range(64))

        if choice < 0.33:
            # ELF header
            buf[0:4] = b"\x7FELF"
        elif choice < 0.66:
            # WAL header
            buf[0:4] = b"WAL\x00"

        test_cases.append(bytes(buf))

    for i, input_data in enumerate(test_cases):
        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_bin],
                input=input_data,
                capture_output=True,
                timeout=1,
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle crashed on input {input_data.hex()}: {e.stderr}")

        # Run student
        try:
            student_proc = subprocess.run(
                [student_bin],
                input=input_data,
                capture_output=True,
                timeout=1
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Student program timed out on input {input_data.hex()}")

        if student_proc.returncode != 0:
            pytest.fail(f"Student program crashed or returned non-zero on input {input_data.hex()}\nStderr: {student_proc.stderr}")

        student_out = student_proc.stdout

        assert student_out == oracle_out, (
            f"Mismatch on iteration {i}.\n"
            f"Input (hex): {input_data.hex()}\n"
            f"Expected output (hex): {oracle_out.hex()}\n"
            f"Actual output (hex): {student_out.hex()}\n"
            f"Expected output (text): {oracle_out}\n"
            f"Actual output (text): {student_out}"
        )