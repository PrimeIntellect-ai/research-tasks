# test_final_state.py

import os
import subprocess
import random
import pytest

def generate_fuzz_inputs(n=5000, seed=42):
    random.seed(seed)
    inputs = []
    ops = ["\\u002B", "\\u002D", "\\u002A"]
    for _ in range(n):
        id_val = random.randint(1, 1000)
        value = random.randint(1, 10000)
        op = random.choice(ops)
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        inputs.append(f"ID={id_val} VALUE={value} OP={op} IP={ip}")
    return "\n".join(inputs) + "\n"

def test_mapper_exists_and_executable():
    student_script = "/home/user/mapper.sh"
    assert os.path.exists(student_script), f"Student script {student_script} does not exist."
    assert os.path.isfile(student_script), f"{student_script} is not a file."
    assert os.access(student_script, os.X_OK), f"{student_script} is not executable."

def test_fuzz_equivalence():
    oracle_script = "/app/oracle_mapper.sh"
    student_script = "/home/user/mapper.sh"

    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} missing."

    input_data = generate_fuzz_inputs(5000, 42)

    # Run oracle
    oracle_proc = subprocess.run(
        ["/bin/bash", oracle_script],
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )
    oracle_output = oracle_proc.stdout

    # Run student
    student_proc = subprocess.run(
        ["/bin/bash", student_script],
        input=input_data,
        text=True,
        capture_output=True
    )

    if student_proc.returncode != 0:
        pytest.fail(f"Student script failed with return code {student_proc.returncode}\nStderr: {student_proc.stderr}")

    student_output = student_proc.stdout

    oracle_lines = oracle_output.strip().split('\n')
    student_lines = student_output.strip().split('\n')
    input_lines = input_data.strip().split('\n')

    assert len(student_lines) == len(oracle_lines), f"Output line count mismatch. Expected {len(oracle_lines)}, got {len(student_lines)}"

    for i, (o_line, s_line) in enumerate(zip(oracle_lines, student_lines)):
        if o_line != s_line:
            pytest.fail(
                f"Mismatch at line {i+1}:\n"
                f"Input:  {input_lines[i]}\n"
                f"Oracle: {o_line}\n"
                f"Agent:  {s_line}"
            )