# test_final_state.py
import os
import json
import random
import string
import subprocess
import pytest

def test_part1_config_json():
    config_path = "/app/services/config.json"
    assert os.path.isfile(config_path), f"{config_path} does not exist"
    with open(config_path, "r") as f:
        data = json.load(f)

    assert data.get("producer_redis_port") == 6379, "producer_redis_port is not correctly set to 6379"
    assert data.get("consumer_redis_port") == 6379, "consumer_redis_port is not correctly set to 6379"

def test_part1_pipeline_success():
    # Run the start script to trigger the pipeline
    start_sh = "/app/services/start.sh"
    assert os.path.isfile(start_sh), f"{start_sh} does not exist"

    result = subprocess.run([start_sh], capture_output=True, text=True)
    assert result.returncode == 0, f"start.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

    log_file = "/home/user/pipeline_success.log"
    assert os.path.isfile(log_file), f"Pipeline success log {log_file} was not created."

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "PIPELINE_OK" in log_content, f"Expected 'PIPELINE_OK' in {log_file}, but found: {log_content}"

def generate_random_fasta():
    num_seqs = random.randint(1, 10)
    out = []
    for _ in range(num_seqs):
        seq_name = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 50)))
        prior = random.uniform(0.0, 1.0)
        out.append(f">{seq_name} prior={prior:.6f}\n")

        seq_len = random.randint(0, 10000)
        chars = ['A', 'C', 'G', 'T', ' ', '\n', 'X', 'Y', 'Z', 'N', '-', '*', '1', '2']
        weights = [20, 20, 20, 20, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1]
        seq = ''.join(random.choices(chars, weights=weights, k=seq_len))
        out.append(seq)
        out.append("\n")
    return "".join(out)

def test_part2_fuzz_equivalence():
    agent_bin = "/home/user/fasta_parser"
    oracle_bin = "/app/oracle_parser"

    assert os.path.isfile(agent_bin), f"Agent binary {agent_bin} does not exist"
    assert os.access(agent_bin, os.X_OK), f"Agent binary {agent_bin} is not executable"

    assert os.path.isfile(oracle_bin), f"Oracle binary {oracle_bin} does not exist"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary {oracle_bin} is not executable"

    random.seed(42)

    for i in range(1000):
        fasta_input = generate_random_fasta()

        try:
            agent_result = subprocess.run(
                [agent_bin],
                input=fasta_input,
                capture_output=True,
                text=True,
                timeout=2
            )
            agent_out = agent_result.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent binary timed out on iteration {i}")

        try:
            oracle_result = subprocess.run(
                [oracle_bin],
                input=fasta_input,
                capture_output=True,
                text=True,
                timeout=2
            )
            oracle_out = oracle_result.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle binary timed out on iteration {i}")

        assert agent_result.returncode == oracle_result.returncode, (
            f"Exit code mismatch on iteration {i}.\n"
            f"Agent exit code: {agent_result.returncode}\n"
            f"Oracle exit code: {oracle_result.returncode}\n"
            f"Input:\n{fasta_input[:500]}..."
        )

        if agent_out != oracle_out:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n"
                f"Input (truncated):\n{fasta_input[:500]}...\n\n"
                f"Oracle Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}"
            )