# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/doc_compiler"
AGENT_SCRIPT = "/home/user/py_compiler.py"
CONFIG_PATH = "/home/user/compiler_config.ini"

def generate_random_string(length):
    return ''.join(random.choices(string.printable, k=length)).encode('utf-8')

def generate_fuzz_inputs(num_cases=100):
    random.seed(42)
    cases = []
    for i in range(num_cases):
        case_type = random.random()

        if case_type < 0.10:
            # Invalid magic bytes
            magic = b"X89TDO\x00" if random.random() < 0.5 else b"random"
            content = magic + b"some_data"
            cases.append(("invalid_magic", content))
        elif case_type < 0.20:
            # Truncated files (no 0xFF)
            content = b"\x89TDOC\x00"
            num_records = random.randint(1, 10)
            for _ in range(num_records):
                rec_type = random.choice([0x01, 0x02, 0x03])
                length = random.randint(0, 50)
                payload = generate_random_string(length)
                content += bytes([rec_type]) + length.to_bytes(2, 'little') + payload
            cases.append(("truncated", content))
        elif case_type < 0.30:
            # Invalid record types
            content = b"\x89TDOC\x00"
            num_records = random.randint(1, 10)
            for _ in range(num_records):
                rec_type = random.choice([0x01, 0x02, 0x03])
                length = random.randint(0, 50)
                payload = generate_random_string(length)
                content += bytes([rec_type]) + length.to_bytes(2, 'little') + payload

            invalid_type = random.choice([t for t in range(256) if t not in [0x01, 0x02, 0x03, 0xFF]])
            length = random.randint(0, 50)
            payload = generate_random_string(length)
            content += bytes([invalid_type]) + length.to_bytes(2, 'little') + payload
            cases.append(("invalid_type", content))
        else:
            # Valid files
            content = b"\x89TDOC\x00"
            num_records = random.randint(1, 50)
            for _ in range(num_records):
                rec_type = random.choice([0x01, 0x02, 0x03])
                length = random.randint(0, 500)
                payload = generate_random_string(length)
                # Ensure we don't accidentally exceed the 2-byte length limit
                length = len(payload)
                content += bytes([rec_type]) + length.to_bytes(2, 'little') + payload
            content += b"\xFF"
            cases.append(("valid", content))

    return cases

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary {ORACLE_PATH} missing."
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} missing."

    inputs = generate_fuzz_inputs(100)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i, (case_type, content) in enumerate(inputs):
            input_file = os.path.join(tmpdir, f"input_{i}.tdoc")
            oracle_out = os.path.join(tmpdir, f"oracle_out_{i}.md")
            agent_out = os.path.join(tmpdir, f"agent_out_{i}.md")

            with open(input_file, "wb") as f:
                f.write(content)

            render_hidden = random.choice([True, False])
            config_content = f"[Settings]\nrender_hidden={'true' if render_hidden else 'false'}\n"
            with open(CONFIG_PATH, "w") as f:
                f.write(config_content)

            oracle_cmd = [ORACLE_PATH, input_file, oracle_out]
            oracle_code, oracle_stdout, oracle_stderr = run_command(oracle_cmd)

            agent_cmd = ["python3", AGENT_SCRIPT, input_file, agent_out]
            agent_code, agent_stdout, agent_stderr = run_command(agent_cmd)

            error_msg = f"Mismatch on test case {i} (type: {case_type}, render_hidden: {render_hidden}).\n"

            assert agent_code == oracle_code, error_msg + f"Exit code mismatch: Oracle={oracle_code}, Agent={agent_code}\nOracle stderr: {oracle_stderr}\nAgent stderr: {agent_stderr}"
            assert agent_stdout == oracle_stdout, error_msg + f"Stdout mismatch: Oracle={repr(oracle_stdout)}, Agent={repr(agent_stdout)}"
            assert agent_stderr == oracle_stderr, error_msg + f"Stderr mismatch: Oracle={repr(oracle_stderr)}, Agent={repr(agent_stderr)}"

            oracle_file_exists = os.path.exists(oracle_out)
            agent_file_exists = os.path.exists(agent_out)

            assert agent_file_exists == oracle_file_exists, error_msg + f"Output file existence mismatch: Oracle={oracle_file_exists}, Agent={agent_file_exists}"

            if oracle_file_exists:
                with open(oracle_out, "rb") as f:
                    oracle_file_content = f.read()
                with open(agent_out, "rb") as f:
                    agent_file_content = f.read()

                assert agent_file_content == oracle_file_content, error_msg + "Output file content mismatch."