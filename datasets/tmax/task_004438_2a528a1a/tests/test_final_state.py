# test_final_state.py
import os
import random
import subprocess
import pytest

def test_router_fuzz_equivalence():
    agent_script = "/home/user/router.sh"
    oracle_script = "/app/oracle_router"

    assert os.path.exists(agent_script), f"Missing {agent_script}"
    assert os.access(agent_script, os.X_OK), f"{agent_script} is not executable"

    random.seed(42)
    for _ in range(500):
        arg1 = random.randint(8000, 48000)
        arg2 = random.randint(1, 2)
        arg3 = random.randint(1, 1000)

        args = [str(arg1), str(arg2), str(arg3)]

        oracle_proc = subprocess.run([oracle_script] + args, capture_output=True, text=True)
        agent_proc = subprocess.run([agent_script] + args, capture_output=True, text=True)

        assert agent_proc.returncode == 0, f"agent script failed on args {args}:\n{agent_proc.stderr}"

        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input {args}. Oracle: '{oracle_out}', Agent: '{agent_out}'"

def test_extract_sh():
    extract_script = "/home/user/extract.sh"
    audio_file = "/app/recording.wav"

    assert os.path.exists(extract_script), f"Missing {extract_script}"
    assert os.access(extract_script, os.X_OK), f"{extract_script} is not executable"

    proc = subprocess.run([extract_script, audio_file], capture_output=True, text=True)
    assert proc.returncode == 0, f"{extract_script} failed:\n{proc.stderr}"

    output = proc.stdout.strip()
    assert output == "44100 2 10", f"Expected extraction output '44100 2 10', got '{output}'"

def test_symlink_created():
    symlink_path = "/home/user/dataset/high_stereo_0/recording.wav"
    target_path = "/app/recording.wav"

    assert os.path.exists(symlink_path), f"Missing symlink or file at {symlink_path}"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"

    actual_target = os.readlink(symlink_path)
    assert actual_target == target_path, f"Symlink points to {actual_target}, expected {target_path}"