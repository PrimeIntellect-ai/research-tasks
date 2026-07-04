# test_final_state.py

import os
import json
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/dataset_packager"
AGENT_PATH = "/home/user/my_packager"
NUM_FUZZ_TESTS = 100

def generate_fuzz_input():
    id_len = random.randint(4, 12)
    id_str = ''.join(random.choices(string.ascii_letters + string.digits, k=id_len))
    cat_len = random.randint(3, 8)
    cat_str = ''.join(random.choices(string.ascii_letters, k=cat_len))
    data_len = random.randint(0, 500)
    data = [random.randint(-10000, 10000) for _ in range(data_len)]
    return {"id": id_str, "category": cat_str, "data": data}

def get_dir_state(d):
    state = {}
    for root, dirs, files in os.walk(d):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, d)
            if os.path.islink(full_path):
                state[rel_path] = ('symlink', os.readlink(full_path))
            else:
                with open(full_path, 'rb') as fp:
                    state[rel_path] = ('file', fp.read())
    return state

def test_agent_executable_exists():
    assert os.path.exists(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not marked as executable"

def test_atomic_write_pattern():
    input_data = generate_fuzz_input()
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "input.json")
        out_dir = os.path.join(tmpdir, "out")
        os.makedirs(out_dir)
        with open(input_file, "w") as f:
            json.dump(input_data, f)

        # Run agent with strace to capture rename syscalls
        strace_cmd = ["strace", "-f", "-e", "trace=rename,renameat,renameat2", AGENT_PATH, input_file, out_dir]
        result = subprocess.run(strace_cmd, capture_output=True, text=True)

        # Check if rename was called involving .tmp
        strace_output = result.stderr
        assert ".tmp" in strace_output and ".bin" in strace_output, \
            "The agent does not appear to use the atomic write pattern (renaming a .tmp file to .bin)."

def test_fuzz_equivalence():
    random.seed(42)

    for i in range(NUM_FUZZ_TESTS):
        input_data = generate_fuzz_input()

        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.json")
            with open(input_file, "w") as f:
                json.dump(input_data, f)

            oracle_out = os.path.join(tmpdir, "oracle_out")
            agent_out = os.path.join(tmpdir, "agent_out")
            os.makedirs(oracle_out)
            os.makedirs(agent_out)

            oracle_res = subprocess.run([ORACLE_PATH, input_file, oracle_out], capture_output=True, text=True)
            assert oracle_res.returncode == 0, f"Oracle failed on input {input_data}"

            agent_res = subprocess.run([AGENT_PATH, input_file, agent_out], capture_output=True, text=True)
            assert agent_res.returncode == 0, f"Agent failed on input {input_data}. Stderr: {agent_res.stderr}"

            oracle_state = get_dir_state(oracle_out)
            agent_state = get_dir_state(agent_out)

            assert oracle_state.keys() == agent_state.keys(), \
                f"Directory structures differ.\nOracle files: {list(oracle_state.keys())}\nAgent files: {list(agent_state.keys())}\nInput: {input_data}"

            for path in oracle_state:
                o_type, o_val = oracle_state[path]
                a_type, a_val = agent_state[path]

                assert o_type == a_type, f"File type mismatch for {path}: oracle={o_type}, agent={a_type}"
                if o_type == 'symlink':
                    assert o_val == a_val, f"Symlink target mismatch for {path}: oracle={o_val}, agent={a_val}"
                else:
                    assert o_val == a_val, f"File content mismatch for {path}. Input: {input_data}"