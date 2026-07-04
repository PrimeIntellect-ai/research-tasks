# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_curated_binaries_directory():
    curated_dir = '/home/user/curated_binaries'
    assert os.path.isdir(curated_dir), f"Directory {curated_dir} does not exist."
    files = os.listdir(curated_dir)
    assert len(files) > 0, f"Directory {curated_dir} is empty. Expected extracted and renamed files."
    for f in files:
        assert f.endswith('-curated.bin'), f"File {f} in {curated_dir} does not have the expected suffix '-curated.bin'."

def test_artifact_namer_executable():
    namer_path = '/home/user/artifact_namer'
    assert os.path.isfile(namer_path), f"Executable {namer_path} does not exist."
    assert os.access(namer_path, os.X_OK), f"File {namer_path} is not executable."

def test_fuzz_equivalence():
    agent_namer = '/home/user/artifact_namer'
    oracle_namer = '/app/oracle_namer'

    assert os.path.isfile(oracle_namer), f"Oracle {oracle_namer} is missing."
    assert os.path.isfile(agent_namer), f"Agent program {agent_namer} is missing."

    random.seed(42)
    chars = string.ascii_letters + string.digits + " _./"

    for i in range(1000):
        length = random.randint(1, 100)
        test_input = "".join(random.choices(chars, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_namer, test_input],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            [agent_namer, test_input],
            capture_output=True,
            text=True
        )
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on input: {repr(test_input)}\n"
            f"Expected (Oracle): {repr(oracle_out)}\n"
            f"Got (Agent):       {repr(agent_out)}"
        )