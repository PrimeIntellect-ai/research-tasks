# test_final_state.py
import os
import random
import subprocess
import string
import pytest

def generate_fuzz_input():
    num_lines = random.randint(10, 100)
    lines = []
    for _ in range(num_lines):
        name_len = random.randint(3, 8)
        name = ''.join(random.choices(string.ascii_lowercase, k=name_len))
        major = random.randint(0, 9)
        minor = random.randint(0, 99)
        patch = random.randint(0, 99)
        lines.append(f"{name} {major}.{minor}.{patch}")
    return "\n".join(lines) + "\n"

def test_build_success():
    build_dir = "/home/user/workspace/build"
    os.makedirs(build_dir, exist_ok=True)

    cmake_res = subprocess.run(["cmake", ".."], cwd=build_dir, capture_output=True, text=True)
    assert cmake_res.returncode == 0, f"CMake failed:\n{cmake_res.stderr}"

    make_res = subprocess.run(["make"], cwd=build_dir, capture_output=True, text=True)
    assert make_res.returncode == 0, f"Make failed:\n{make_res.stderr}"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/resolve_oracle.py"
    agent_script = "/home/user/workspace/resolve.py"

    assert os.path.isfile(oracle_path), f"Oracle script missing at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)

    for i in range(50):
        input_data = generate_fuzz_input()

        oracle_res = subprocess.run(
            ["python3", oracle_path],
            input=input_data,
            capture_output=True,
            text=True
        )

        agent_res = subprocess.run(
            ["python3", agent_script],
            input=input_data,
            cwd="/home/user/workspace",
            capture_output=True,
            text=True
        )

        assert agent_res.returncode == 0, f"Agent script failed on run {i} with error:\n{agent_res.stderr}\nInput:\n{input_data}"
        assert oracle_res.returncode == 0, f"Oracle script failed on run {i} with error:\n{oracle_res.stderr}"

        assert agent_res.stdout == oracle_res.stdout, f"Mismatch on run {i}.\nInput:\n{input_data}\nOracle Output:\n{oracle_res.stdout}\nAgent Output:\n{agent_res.stdout}"