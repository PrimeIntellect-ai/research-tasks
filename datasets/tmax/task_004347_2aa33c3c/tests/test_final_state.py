# test_final_state.py

import os
import struct
import random
import subprocess
import tempfile
import pytest

def generate_fuzz_input(filename, length):
    with open(filename, 'wb') as f:
        # Using native byte order as both C and Python will run on the same architecture
        f.write(struct.pack('4sI', b'SENS', length))
        if length > 0:
            floats = [random.uniform(-1e6, 1e6) for _ in range(length)]
            f.write(struct.pack(f'{length}d', *floats))

def test_fuzz_equivalence():
    """Verify that the agent's Python program matches the C oracle bit-exactly on random inputs."""
    random.seed(42)
    oracle = "/app/bin/legacy_calc_ref"
    assert os.path.isfile(oracle), "Oracle binary not found."

    agent_cmd = ["python", "-m", "calc_core.cli"]
    agent_env = os.environ.copy()
    agent_env["PYTHONPATH"] = "/app/calc_core-1.2.3"
    agent_env["CALC_LOG_DIR"] = "/tmp"

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(100):
            if i == 0:
                length = 0
            elif i == 1:
                length = 1
            else:
                length = random.randint(2, 10000)

            input_file = os.path.join(tmpdir, f"test_{i}.bin")
            generate_fuzz_input(input_file, length)

            oracle_proc = subprocess.run([oracle, input_file], capture_output=True, text=True)
            agent_proc = subprocess.run(agent_cmd + [input_file], env=agent_env, capture_output=True, text=True)

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Return code mismatch on input {i} (length {length}): "
                f"agent={agent_proc.returncode}, oracle={oracle_proc.returncode}\n"
                f"Agent stderr: {agent_proc.stderr}\nOracle stderr: {oracle_proc.stderr}"
            )

            assert agent_proc.stdout == oracle_proc.stdout, (
                f"Output mismatch on input {i} (length {length}):\n"
                f"Agent output:\n{agent_proc.stdout}\n"
                f"Oracle output:\n{oracle_proc.stdout}"
            )

def test_regression_script():
    """Verify that the regression script exists and generates the expected files."""
    script_path = "/home/user/regression.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    env = os.environ.copy()
    env["PYTHONPATH"] = "/app/calc_core-1.2.3"
    env["CALC_LOG_DIR"] = "/tmp"

    test_bin = "/home/user/test.bin"
    log_txt = "/home/user/regression_log.txt"

    if os.path.exists(test_bin):
        os.remove(test_bin)
    if os.path.exists(log_txt):
        os.remove(log_txt)

    proc = subprocess.run(["python", script_path], env=env, capture_output=True, text=True)
    assert proc.returncode == 0, f"regression.py failed with return code {proc.returncode}:\n{proc.stderr}"

    assert os.path.isfile(test_bin), f"regression.py did not create {test_bin}."
    assert os.path.isfile(log_txt), f"regression.py did not create {log_txt}."