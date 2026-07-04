# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_part1_log_merger():
    merged_log = "/home/user/merged_access.log"
    assert os.path.exists(merged_log), f"{merged_log} does not exist."
    assert os.path.getsize(merged_log) > 0, f"{merged_log} is empty."

    binary = "/home/user/log_merger/log_merger"
    assert os.path.exists(binary), f"{binary} does not exist. Did you run make?"
    assert os.access(binary, os.X_OK), f"{binary} is not executable."

def generate_fuzz_strings(n=2000):
    random.seed(42)
    chars = string.ascii_letters + string.digits + "/.%<>_-"

    # special components to inject to bias towards url encoding and edge cases
    components = [
        "../", ".env", ".php", "<script>", "admin/",
        "%2e%2e%2f", "%2E%2E%2F", "%2eenv", "%2Ephp", "%3cscript%3e", "admin%2f",
        "//", "///", "/./", "/../", "/a/b/./c//d/",
        "a", "b", "1", "2"
    ]

    payloads = []
    for _ in range(n):
        length = random.randint(1, 255)
        parts = []
        cur_len = 0
        while cur_len < length:
            if random.random() < 0.5:
                comp = random.choice(components)
            else:
                comp = "".join(random.choices(chars, k=random.randint(1, 10)))
            if cur_len + len(comp) > length:
                comp = comp[:length - cur_len]
            parts.append(comp)
            cur_len += len(comp)

        payloads.append("".join(parts))
    return payloads

def test_part2_waf_evaluator_fuzz():
    agent_script = "/home/user/waf_eval_pure.sh"
    oracle_bin = "/app/waf_evaluator_stripped"

    assert os.path.exists(agent_script), f"{agent_script} does not exist."

    payloads = generate_fuzz_strings(2000)

    for payload in payloads:
        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, payload],
            capture_output=True,
            text=True
        )
        oracle_out = oracle_proc.stdout.strip()
        oracle_code = oracle_proc.returncode

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_script, payload],
            capture_output=True,
            text=True
        )
        agent_out = agent_proc.stdout.strip()
        agent_code = agent_proc.returncode

        assert oracle_code == agent_code, f"Exit code mismatch on payload: {repr(payload)}\nOracle exited with {oracle_code}, Agent exited with {agent_code}\nOracle stdout: {oracle_out}\nAgent stdout: {agent_out}"
        assert oracle_out == agent_out, f"Stdout mismatch on payload: {repr(payload)}\nOracle stdout: {repr(oracle_out)}\nAgent stdout: {repr(agent_out)}"