# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_libcsv_ext_built():
    lib_path = "/app/libcsv_ext-1.0.0/libcsv_ext.a"
    assert os.path.isfile(lib_path), f"Library {lib_path} was not built."

def test_processor_exists_and_executable():
    processor_path = "/home/user/processor"
    assert os.path.isfile(processor_path), f"Processor program {processor_path} is missing."
    assert os.access(processor_path, os.X_OK), f"Processor program {processor_path} is not executable."

def generate_csv_data(seed):
    random.seed(seed)
    num_lines = random.randint(0, 100)
    lines = []
    for _ in range(num_lines):
        if random.random() < 0.2:
            id_val = random.randint(-1000, -1)
        else:
            id_val = random.randint(0, 1000)

        val = random.uniform(-1000.0, 1000.0)

        if random.random() < 0.9:
            cat = random.choice(['A', 'B', 'C'])
        else:
            # random ascii character
            cat = random.choice(string.ascii_letters + string.digits + "!@#$%^&*()_+{}|:\"<>?-=[]\\;',./")

        score = random.uniform(-1.0, 2.0)

        lines.append(f"{id_val},{val},{cat},{score}")
    return "\n".join(lines) + ("\n" if lines else "")

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/processor"

    assert os.path.isfile(oracle_path), "Oracle program missing."
    assert os.path.isfile(agent_path), "Agent program missing."

    for i in range(500):
        input_data = generate_csv_data(seed=i)

        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data.encode("utf-8"),
            capture_output=True
        )
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data.encode("utf-8"),
            capture_output=True
        )

        oracle_out = oracle_proc.stdout.decode("utf-8")
        agent_out = agent_proc.stdout.decode("utf-8")

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input:\n{input_data}\n"
                f"Expected Output (Oracle):\n{oracle_out}\n"
                f"Actual Output (Agent):\n{agent_out}\n"
            )