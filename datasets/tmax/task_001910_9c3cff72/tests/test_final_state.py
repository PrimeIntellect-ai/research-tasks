# test_final_state.py

import os
import random
import subprocess
import pytest

N = 5000
MIN_LEN = 4
MAX_LEN = 256
ORACLE = "/app/oracle_decoder"
AGENT_SCRIPT = "/home/user/clean_decoder.py"

def test_agent_script_exists():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    assert os.path.isfile(AGENT_SCRIPT), f"{AGENT_SCRIPT} is not a file"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE), f"Oracle not found at {ORACLE}"
    assert os.path.exists(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

    random.seed(42)

    # Generate random inputs and some crafted inputs to ensure overflow is triggered
    inputs = []
    for _ in range(N):
        length = random.randint(MIN_LEN, MAX_LEN)
        inputs.append(bytes(random.choices(range(256), k=length)))

    # Add a few crafted inputs with specific lengths to test the overflow boundary
    # L * 2 + 2147483640 > 2147483647 => L > 3
    # L is a 4-byte signed little-endian integer.
    for l_val in [2, 3, 4, 5, 10, 100]:
        payload_len = max(l_val, 0)
        if payload_len + 4 <= MAX_LEN:
            prefix = l_val.to_bytes(4, byteorder='little', signed=True)
            body = bytes(random.choices(range(256), k=payload_len))
            inputs.append(prefix + body)

    for idx, input_data in enumerate(inputs):
        oracle_proc = subprocess.run(
            [ORACLE],
            input=input_data,
            capture_output=True
        )

        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT],
            input=input_data,
            capture_output=True
        )

        msg_base = f"Mismatch on input #{idx} (hex: {input_data.hex()})"
        assert oracle_proc.returncode == agent_proc.returncode, f"{msg_base}: Return code oracle={oracle_proc.returncode}, agent={agent_proc.returncode}"
        assert oracle_proc.stdout == agent_proc.stdout, f"{msg_base}: Stdout oracle={oracle_proc.stdout.hex()}, agent={agent_proc.stdout.hex()}"