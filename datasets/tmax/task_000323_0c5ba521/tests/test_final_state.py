# test_final_state.py

import os
import time
import json
import random
import subprocess
import urllib.request
import pytest
import signal

def generate_fuzz_inputs(n=10000, seed=42):
    random.seed(seed)
    base_string = b"[2023-10-01T12:00:00] INFO - Application started normally."
    inputs = [b""]

    for _ in range(n - 1):
        length = random.randint(1, 1024)
        if random.random() < 0.1:
            # Random bytes
            inp = bytes(random.choices(range(256), k=length))
        else:
            # Mutate base string
            inp = bytearray(base_string)
            num_mutations = random.randint(1, 10)
            for _ in range(num_mutations):
                mut_type = random.randint(0, 3)
                if mut_type == 0 and len(inp) > 0:
                    # bit flip
                    idx = random.randint(0, len(inp) - 1)
                    inp[idx] ^= (1 << random.randint(0, 7))
                elif mut_type == 1 and len(inp) > 0:
                    # delete
                    idx = random.randint(0, len(inp) - 1)
                    del inp[idx]
                elif mut_type == 2:
                    # duplicate
                    if len(inp) > 0:
                        idx = random.randint(0, len(inp) - 1)
                        inp.insert(idx, inp[idx])
                elif mut_type == 3:
                    # insert random char
                    idx = random.randint(0, len(inp))
                    inp.insert(idx, random.randint(0, 255))
            inp = bytes(inp[:1024])
        inputs.append(inp)
    return inputs

def test_fuzz_equivalence():
    oracle_path = "/home/user/oracle/parser_oracle"
    agent_path = "/home/user/app/parser.py"

    assert os.path.isfile(oracle_path), "Oracle binary not found"
    assert os.path.isfile(agent_path), "Agent parser script not found"

    inputs = generate_fuzz_inputs(n=10000)

    for i, inp in enumerate(inputs):
        # Run oracle
        proc_oracle = subprocess.run([oracle_path], input=inp, capture_output=True)
        oracle_out = proc_oracle.stdout

        # Run agent
        proc_agent = subprocess.run(["python3", agent_path], input=inp, capture_output=True)
        agent_out = proc_agent.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on input {i}:\n"
                f"Input (hex): {inp.hex()}\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output: {agent_out}"
            )

def test_end_to_end_flow():
    start_sh = "/home/user/app/start.sh"
    parsed_logs = "/home/user/app/parsed_logs.json"

    if os.path.exists(parsed_logs):
        os.remove(parsed_logs)

    # Start the services
    process = subprocess.Popen(["bash", start_sh], preexec_fn=os.setsid)

    try:
        time.sleep(2)

        # Send POST request
        url = "http://localhost:8080/ingest"
        data = json.dumps({"raw_log": "[2023-10-01T12:00:00] INFO - e2e test"}).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

        try:
            with urllib.request.urlopen(req) as response:
                assert response.status == 200, "API did not return 200 OK"
        except Exception as e:
            pytest.fail(f"Failed to send POST request to API: {e}")

        time.sleep(2)

        assert os.path.exists(parsed_logs), f"{parsed_logs} was not created"

        with open(parsed_logs, "r") as f:
            content = f.read()

        expected = '{"timestamp": "2023-10-01T12:00:00", "level": "INFO", "message": "e2e test"}\n'
        assert expected in content, f"Expected log not found in {parsed_logs}. Content: {content}"

    finally:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)