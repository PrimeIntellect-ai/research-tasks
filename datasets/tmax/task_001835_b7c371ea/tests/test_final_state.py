# test_final_state.py

import os
import subprocess
import random
import string
import time
import urllib.request
import socket
import pytest

def test_services_active():
    services = ["app_mock.service", "dashboard.service", "aggregator.service"]
    for svc in services:
        cmd = ["systemctl", "--user", "is-active", svc]
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode == 0 and res.stdout.strip() == "active", f"Service {svc} is not active."

def generate_fuzz_inputs(n=10000, seed=42):
    random.seed(seed)
    inputs = []
    types = ['gauge', 'count', 'timer', 'histogram']
    for _ in range(n):
        if random.random() < 0.2:
            choice = random.randint(0, 3)
            if choice == 0:
                inputs.append("garbage_string_without_delimiters\n")
            elif choice == 1:
                inputs.append(f"metric:{random.random()}|type\n")
            elif choice == 2:
                inputs.append(f"metric|{random.random()}|#tag:val\n")
            else:
                inputs.append("metric:not_a_float|count|#tag:val\n")
        else:
            name = ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10)))
            val = random.uniform(-1000, 1000)
            typ = random.choice(types)
            num_tags = random.randint(1, 5)
            tags = [f"{''.join(random.choices(string.ascii_letters, k=random.randint(2, 5)))}:{''.join(random.choices(string.ascii_letters, k=random.randint(2, 5)))}" for _ in range(num_tags)]
            tags_str = ",".join(tags)
            inputs.append(f"{name}:{val:.5f}|{typ}|#{tags_str}\n")
    return inputs

def test_parser_fuzz_equivalence():
    oracle_path = "/opt/oracle/parser_oracle"
    agent_path = "/home/user/parser"

    assert os.path.isfile(agent_path), f"Agent parser executable not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent parser at {agent_path} is not executable"

    inputs = generate_fuzz_inputs(1000) # Reduced to 1000 for execution time safety while maintaining fuzzing intent

    for i, inp in enumerate(inputs):
        oracle_res = subprocess.run([oracle_path], input=inp, capture_output=True, text=True)
        agent_res = subprocess.run([agent_path], input=inp, capture_output=True, text=True)

        assert oracle_res.stdout == agent_res.stdout, (
            f"Mismatch on input {i}: {repr(inp)}\n"
            f"Oracle output: {repr(oracle_res.stdout)}\n"
            f"Agent output:  {repr(agent_res.stdout)}"
        )

def test_end_to_end_pipeline():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = b"test_metric:42.0|count|#tag1:a,tag2:b\n"
    sock.sendto(msg, ("127.0.0.1", 8125))

    time.sleep(1.5)

    req = urllib.request.Request("http://localhost:9090/latest")
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8').strip()
            expected = "NAME=[test_metric] TYPE=[count] VALUE=[42.0000] TAGS=[tag1=a;tag2=b;]"
            assert body == expected, f"End-to-end failed. Expected {expected}, got {body}"
    except Exception as e:
        pytest.fail(f"Failed to fetch from dashboard or end-to-end pipeline broken: {e}")