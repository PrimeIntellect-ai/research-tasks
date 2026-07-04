# test_final_state.py

import os
import random
import subprocess
import pytest

def test_decoder_exists_and_executable():
    student_exe = "/home/user/decoder"
    assert os.path.isfile(student_exe), f"Student executable {student_exe} is missing."
    assert os.access(student_exe, os.X_OK), f"Student executable {student_exe} is not executable."

def test_fuzz_equivalence():
    oracle_exe = "/app/oracle_decoder"
    student_exe = "/home/user/decoder"

    assert os.path.isfile(oracle_exe), f"Oracle executable {oracle_exe} is missing."
    assert os.access(oracle_exe, os.X_OK), f"Oracle executable {oracle_exe} is not executable."

    # Use a fixed seed for reproducibility
    rng = random.Random(42)

    N = 10000
    for i in range(N):
        length = rng.randint(16, 1024)
        input_data = bytearray(rng.getrandbits(8) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_exe],
            input=input_data,
            capture_output=True
        )

        # Run student
        student_proc = subprocess.run(
            [student_exe],
            input=input_data,
            capture_output=True
        )

        # Assert return codes match
        assert student_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on fuzz iteration {i}.\n"
            f"Input length: {length}\n"
            f"Oracle return code: {oracle_proc.returncode}\n"
            f"Student return code: {student_proc.returncode}\n"
        )

        # Assert stdout matches
        assert student_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on fuzz iteration {i}.\n"
            f"Input length: {length}\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Student stdout: {student_proc.stdout!r}\n"
        )