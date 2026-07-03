# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def generate_random_path():
    chars = string.ascii_letters + string.digits + " _-!@#"
    name = "".join(random.choice(chars) for _ in range(15))
    return f"/tmp/{name}.mp4"

def test_fuzz_equivalence():
    agent_script = "/home/user/extract_metadata_fixed.py"
    oracle_bin = "/app/bin/extract_metadata_oracle"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle not found at {oracle_bin}"

    random.seed(42)

    # Generate 100 inputs
    paths = ["/app/incident_evidence.mp4"] * 20
    for _ in range(80):
        paths.append(generate_random_path())

    random.shuffle(paths)

    for i in range(100):
        path = paths[i]
        offset = random.randint(-10000, 10000)

        # Run oracle
        oracle_cmd = [oracle_bin, path, str(offset)]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)

        # Run agent
        agent_cmd = ["python3", agent_script, path, str(offset)]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert agent_res.stdout == oracle_res.stdout, (
            f"Output mismatch on run {i+1}/100.\n"
            f"Input path: '{path}'\n"
            f"Input offset: {offset}\n"
            f"Oracle stdout:\n{oracle_res.stdout}\n"
            f"Agent stdout:\n{agent_res.stdout}"
        )