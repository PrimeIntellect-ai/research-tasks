# test_final_state.py

import os
import subprocess
import random

def test_fuzz_calc_similarity():
    """Fuzz test the agent's C program against the oracle."""
    agent_bin = "/home/user/calc_similarity"
    oracle_bin = "/app/oracle_calc"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    random.seed(42)
    for i in range(500):
        num_lines = random.randint(1, 50)
        lines = []
        for _ in range(num_lines):
            # 10% chance to have a count not a multiple of 3
            if random.random() < 0.1:
                count = random.randint(1, 300)
                while count % 3 == 0:
                    count = random.randint(1, 300)
            else:
                count = random.randint(1, 100) * 3

            vals = [str(random.randint(-100, 300)) for _ in range(count)]
            lines.append(" ".join(vals))

        input_data = "\n".join(lines) + "\n"

        oracle_proc = subprocess.run([oracle_bin], input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run([agent_bin], input=input_data, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, "Oracle program failed unexpectedly."
        assert agent_proc.returncode == 0, f"Agent program failed on input:\n{input_data}"

        if oracle_proc.stdout != agent_proc.stdout:
            assert False, (
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input:\n{input_data}\n"
                f"Oracle Output:\n{oracle_proc.stdout}\n"
                f"Agent Output:\n{agent_proc.stdout}"
            )

def test_pipeline_script_exists():
    """Check if the pipeline script exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"Pipeline script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script at {script_path} is not executable"

def test_pipeline_artifacts():
    """Verify that the pipeline produced the correct wide format RGB and distances files."""
    rgb_path = "/home/user/rgb_wide.txt"
    dist_path = "/home/user/distances.txt"
    oracle_bin = "/app/oracle_calc"

    assert os.path.exists(rgb_path), f"{rgb_path} is missing"
    assert os.path.exists(dist_path), f"{dist_path} is missing"

    with open(rgb_path, "r") as f:
        rgb_data = f.read()

    tokens = rgb_data.split()
    assert len(tokens) >= 15, "rgb_wide.txt should contain at least 15 integers (for 5 seconds of video at 1fps)"
    assert len(tokens) % 3 == 0, "rgb_wide.txt should contain a multiple of 3 integers"

    for token in tokens:
        assert token.lstrip('-').isdigit(), f"Non-integer token found in rgb_wide.txt: {token}"

    oracle_proc = subprocess.run([oracle_bin], input=rgb_data, text=True, capture_output=True)
    assert oracle_proc.returncode == 0, "Oracle failed to process rgb_wide.txt"

    with open(dist_path, "r") as f:
        agent_out = f.read()

    assert oracle_proc.stdout == agent_out, (
        f"Contents of {dist_path} do not match expected output for the generated {rgb_path}.\n"
        f"Expected:\n{oracle_proc.stdout}\n"
        f"Actual:\n{agent_out}"
    )