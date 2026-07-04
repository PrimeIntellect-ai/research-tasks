# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

def test_config_updated():
    """Check if the API secret was correctly rotated in the configuration file."""
    config_path = "/app/config/settings.json"
    assert os.path.isfile(config_path), f"{config_path} is missing."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {config_path} as JSON.")

    assert config.get("api_secret") == "Secr3t_HMAC_v2_991", (
        "The 'api_secret' in settings.json was not updated to the correct value."
    )

def test_redis_session_revoked():
    """Check if the compromised session keys were removed from Redis."""
    # We use redis-cli to check if the keys exist
    try:
        res_a = subprocess.run(["redis-cli", "exists", "session:tok_compromised_a"], capture_output=True, text=True, check=True)
        assert res_a.stdout.strip() == "0", "Compromised Redis key 'session:tok_compromised_a' was not deleted."

        res_b = subprocess.run(["redis-cli", "exists", "session:tok_compromised_b"], capture_output=True, text=True, check=True)
        assert res_b.stdout.strip() == "0", "Compromised Redis key 'session:tok_compromised_b' was not deleted."
    except FileNotFoundError:
        # If redis-cli is not installed in the test container, we skip this assertion.
        pass

def test_fuzz_equivalence():
    """Fuzz test the student's token generation script against the reference oracle."""
    agent_script = "/home/user/generate_token.py"
    oracle_script = "/app/oracle/reference_token_gen"

    assert os.path.isfile(agent_script), f"The script {agent_script} does not exist."
    assert os.path.isfile(oracle_script), f"The oracle {oracle_script} does not exist."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for i in range(500):
        user_len = random.randint(4, 20)
        fuzz_user = "".join(random.choices(charset, k=user_len))
        fuzz_time = str(random.randint(1600000000, 1800000000))

        cmd_oracle = [oracle_script, "--user", fuzz_user, "--time", fuzz_time]
        cmd_agent = ["python3", agent_script, "--user", fuzz_user, "--time", fuzz_time]

        res_oracle = subprocess.run(cmd_oracle, capture_output=True, text=True)
        assert res_oracle.returncode == 0, f"Oracle failed unexpectedly on input --user {fuzz_user} --time {fuzz_time}"

        res_agent = subprocess.run(cmd_agent, capture_output=True, text=True)
        assert res_agent.returncode == 0, (
            f"Agent script failed on input --user {fuzz_user} --time {fuzz_time}.\n"
            f"Stderr: {res_agent.stderr}"
        )

        out_oracle = res_oracle.stdout.strip()
        out_agent = res_agent.stdout.strip()

        assert out_agent == out_oracle, (
            f"Output mismatch on fuzz iteration {i+1}.\n"
            f"Input: --user {fuzz_user} --time {fuzz_time}\n"
            f"Expected (Oracle): {out_oracle}\n"
            f"Got (Agent): {out_agent}"
        )