# test_final_state.py
import json
import random
import subprocess
import os
import pytest

def generate_random_transactions(num_tx):
    accounts = list("ABCDEFGHIJKLMNOPQRST")
    transactions = []
    for i in range(num_tx):
        src = random.choice(accounts)
        dst = random.choice(accounts)
        while dst == src:
            dst = random.choice(accounts)
        amount = random.randint(100, 15000)
        transactions.append({
            "tx_id": f"T{i}",
            "from_acct": src,
            "to_acct": dst,
            "amount": amount
        })
    return transactions

def test_agent_script_exists():
    assert os.path.isfile("/home/user/audit.py"), "The agent script /home/user/audit.py does not exist."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/audit_oracle.py"
    agent_script = "/home/user/audit.py"

    assert os.path.isfile(oracle_path), f"Oracle program not found at {oracle_path}"

    random.seed(42)
    N = 100  # Run 100 iterations to avoid excessive test duration, while still providing good coverage

    for _ in range(N):
        num_tx = random.randint(5, 50)
        tx_data = generate_random_transactions(num_tx)
        input_json = json.dumps(tx_data)

        oracle_cmd = ["/usr/bin/python3", oracle_path, input_json]
        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, timeout=5)
            oracle_out = oracle_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle timed out. This is unexpected.")

        agent_cmd = ["/usr/bin/python3", agent_script, input_json]
        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, timeout=5)
            agent_out = agent_res.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent timed out on input: {input_json}\nThis is likely due to the deadlock bug in the vendored package not being properly fixed.")

        assert agent_res.returncode == oracle_res.returncode, (
            f"Return code mismatch on input {input_json}\n"
            f"Oracle returncode: {oracle_res.returncode}\n"
            f"Agent returncode: {agent_res.returncode}\n"
            f"Oracle stderr: {oracle_res.stderr}\n"
            f"Agent stderr: {agent_res.stderr}"
        )

        if oracle_res.returncode == 0:
            assert agent_out == oracle_out, (
                f"Output mismatch on input {input_json}\n"
                f"Oracle output: {oracle_out}\n"
                f"Agent output: {agent_out}"
            )