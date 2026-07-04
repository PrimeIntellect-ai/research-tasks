# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_directories_created():
    expected_dirs = [
        "/home/user/spool",
        "/home/user/spool/incoming",
        "/home/user/spool/processed",
        "/home/user/spool/failed"
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Expected directory missing: {d}"

def test_symlink_created():
    symlink_path = "/home/user/data_in"
    assert os.path.islink(symlink_path), f"Expected symlink missing: {symlink_path}"
    target = os.readlink(symlink_path)
    abs_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    assert abs_target == "/home/user/spool/incoming", f"Symlink points to wrong target: {target}"

def test_telemetry_processor_fuzz_equivalence():
    agent_script = "/home/user/telemetry_processor.py"
    oracle_bin = "/app/oracle_daemon"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_bin), f"Oracle binary missing: {oracle_bin}"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for i in range(500):
        length = random.randint(10, 200)
        test_input = "".join(random.choices(charset, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=test_input,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=test_input,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed on input: {test_input}\nStderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout.strip()

        assert agent_output == oracle_output, (
            f"Output mismatch on input: {test_input}\n"
            f"Expected (Oracle): {oracle_output}\n"
            f"Got (Agent): {agent_output}"
        )