# test_final_state.py

import os
import random
import base64
import subprocess
import pytest
import concurrent.futures

AGENT_SCRIPT = "/home/user/final_parser.py"
ORACLE_SCRIPT = "/app/oracle_parser.pyc"

def generate_fuzz_inputs(n=5000):
    random.seed(42)
    inputs = []
    for _ in range(n):
        if random.random() < 0.5:
            # Corrupted length: array length must be < 255 so byte[0] can be > length
            length = random.randint(5, 254)
            data = bytearray(random.getrandbits(8) for _ in range(length))
            data[0] = random.randint(length + 1, 255)
        else:
            # Normal or other cases
            length = random.randint(5, 1024)
            data = bytearray(random.getrandbits(8) for _ in range(length))
            data[0] = random.randint(0, min(length, 255))
        inputs.append(base64.b64encode(data).decode('utf-8'))
    return inputs

def run_script(script_path, arg):
    try:
        result = subprocess.run(
            ["python3", script_path, arg],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"

def test_final_parser_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Missing required file: {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"Path is not a file: {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script not found at {ORACLE_SCRIPT}"

    inputs = generate_fuzz_inputs(5000)

    # We can use ThreadPoolExecutor to speed up the 5000 subprocess calls
    def check_input(b64_input):
        oracle_code, oracle_out, oracle_err = run_script(ORACLE_SCRIPT, b64_input)
        agent_code, agent_out, agent_err = run_script(AGENT_SCRIPT, b64_input)

        if oracle_out != agent_out:
            return b64_input, oracle_out, agent_out
        return None

    mismatches = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        results = executor.map(check_input, inputs)
        for res in results:
            if res is not None:
                mismatches.append(res)
                if len(mismatches) >= 5:  # stop collecting after 5 to avoid huge output
                    break

    if mismatches:
        error_msg = "Fuzz equivalence failed. Mismatches found:\n"
        for b64_input, oracle_out, agent_out in mismatches:
            error_msg += f"Input: {b64_input}\nOracle: {oracle_out}\nAgent:  {agent_out}\n\n"
        pytest.fail(error_msg)