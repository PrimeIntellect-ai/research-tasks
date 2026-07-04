# test_final_state.py
import json
import os
import random
import string
import subprocess
import pytest

def generate_random_dag():
    num_nodes = random.randint(5, 20)
    nodes = []
    ops = ["duration", "peak", "rms", "zcr"]
    created_ids = []

    for i in range(num_nodes):
        node_id = f"task_{i}_" + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        op = random.choice(ops)

        deps = []
        if created_ids:
            num_deps = random.randint(0, min(3, len(created_ids)))
            deps = random.sample(created_ids, num_deps)

        nodes.append({"id": node_id, "op": op, "deps": deps})
        created_ids.append(node_id)

    random.shuffle(nodes)
    return json.dumps(nodes)

def test_fuzz_equivalence():
    agent_script = "/home/user/py3_audio_processor.py"
    oracle_binary = "/app/oracle_audio_graph"
    audio_file = "/app/interview.wav"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.isfile(oracle_binary), f"Oracle binary not found at {oracle_binary}"
    assert os.path.isfile(audio_file), f"Audio fixture not found at {audio_file}"

    random.seed(42)

    for i in range(100):
        graph_json = generate_random_dag()

        oracle_cmd = [oracle_binary, "--audio", audio_file, "--graph", graph_json]
        agent_cmd = ["python3", agent_script, "--audio", audio_file, "--graph", graph_json]

        oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input {graph_json}\nStderr: {oracle_proc.stderr}"
        assert agent_proc.returncode == 0, f"Agent script failed on input {graph_json}\nStderr: {agent_proc.stderr}"

        try:
            oracle_out = json.loads(oracle_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle output invalid JSON: {oracle_proc.stdout}")

        try:
            agent_out = json.loads(agent_proc.stdout)
        except json.JSONDecodeError:
            pytest.fail(f"Agent output invalid JSON: {agent_proc.stdout}")

        assert agent_out == oracle_out, (
            f"Output mismatch on run {i + 1}/100!\n"
            f"Graph JSON: {graph_json}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}"
        )