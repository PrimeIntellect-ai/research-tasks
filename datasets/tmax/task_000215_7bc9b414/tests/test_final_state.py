# test_final_state.py

import os
import random
import string
import subprocess
import urllib.request
import urllib.error
import json
import pytest
import tempfile
import shutil

ORACLE_PATH = "/app/oracle_analyzer_cli"
AGENT_PATH = "/home/user/build_analyzer/build/analyzer_cli"

def generate_random_node():
    length = random.randint(1, 10)
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def generate_fuzz_inputs(n=1000):
    random.seed(42)
    inputs = []
    for _ in range(n):
        r = random.random()
        if r < 0.1:
            # single node or empty
            if random.random() < 0.5:
                inputs.append("")
            else:
                inputs.append(generate_random_node())
        elif r < 0.4:
            # cycles
            num_nodes = random.randint(2, 10)
            nodes = [generate_random_node() for _ in range(num_nodes)]
            edges = []
            for i in range(num_nodes):
                edges.append(f"{nodes[i]}->{nodes[(i+1)%num_nodes]}")
            for _ in range(random.randint(0, 5)):
                edges.append(f"{random.choice(nodes)}->{random.choice(nodes)}")
            inputs.append(", ".join(edges))
        else:
            # acyclic or random
            num_nodes = random.randint(2, 10)
            nodes = [generate_random_node() for _ in range(num_nodes)]
            edges = []
            for i in range(num_nodes):
                for j in range(i+1, num_nodes):
                    if random.random() < 0.3:
                        edges.append(f"{nodes[i]}->{nodes[j]}")
            inputs.append(", ".join(edges))
    return inputs

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary not executable"

    assert os.path.isfile(AGENT_PATH), f"Agent binary missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary not executable"

    inputs = generate_fuzz_inputs(1000)

    for i, inp in enumerate(inputs):
        oracle_proc = subprocess.run([ORACLE_PATH, inp], capture_output=True, text=True)
        agent_proc = subprocess.run([AGENT_PATH, inp], capture_output=True, text=True)

        assert oracle_proc.returncode == agent_proc.returncode, \
            f"Return code mismatch on input '{inp}'. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        assert oracle_proc.stdout == agent_proc.stdout, \
            f"Output mismatch on input '{inp}'.\nOracle:\n{oracle_proc.stdout}\nAgent:\n{agent_proc.stdout}"

def test_api_server_running():
    url = "http://localhost:8080/analyze"
    data = b"A->B, B->C, C->A"
    req = urllib.request.Request(url, data=data, method='POST')

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            resp_body = response.read().decode('utf-8')
            try:
                json_data = json.loads(resp_body)
                assert isinstance(json_data, dict), "Response should be a JSON object"
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON response from API: {resp_body}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API on port 8080: {e}")

def test_cross_compilation_support():
    source_dir = "/home/user/build_analyzer"
    assert os.path.isdir(source_dir), f"Source directory {source_dir} missing"

    with tempfile.TemporaryDirectory() as build_dir:
        cmake_cmd = ["cmake", f"-DTARGET_ARCH=aarch64", source_dir]
        cmake_proc = subprocess.run(cmake_cmd, cwd=build_dir, capture_output=True, text=True)
        assert cmake_proc.returncode == 0, f"CMake failed for aarch64:\n{cmake_proc.stderr}"

        make_cmd = ["make"]
        make_proc = subprocess.run(make_cmd, cwd=build_dir, capture_output=True, text=True)
        assert make_proc.returncode == 0, f"Make failed for aarch64:\n{make_proc.stderr}"

        binary_path = os.path.join(build_dir, "analyzer_cli")
        assert os.path.isfile(binary_path), "analyzer_cli binary not produced during cross-compilation"

        file_cmd = ["file", binary_path]
        file_proc = subprocess.run(file_cmd, capture_output=True, text=True)
        assert "aarch64" in file_proc.stdout.lower() or "arm64" in file_proc.stdout.lower(), \
            f"Binary is not compiled for aarch64. File output: {file_proc.stdout}"