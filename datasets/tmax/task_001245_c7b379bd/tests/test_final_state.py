# test_final_state.py
import os
import json
import random
import subprocess
import pytest

def test_bash_profile_exports():
    """Verify that the required environment variables are exported in .bash_profile."""
    bash_profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(bash_profile_path), f"Missing {bash_profile_path}"

    with open(bash_profile_path, "r") as f:
        content = f.read()

    assert "ZONE_A_BASE=14" in content, "ZONE_A_BASE is not correctly exported in .bash_profile"
    assert "ZONE_B_BASE=9" in content, "ZONE_B_BASE is not correctly exported in .bash_profile"
    assert "ZONE_C_BASE=18" in content, "ZONE_C_BASE is not correctly exported in .bash_profile"

def test_setup_proxy_script():
    """Verify setup_proxy.sh creates the correct firewall_rules.txt."""
    script_path = "/home/user/setup_proxy.sh"
    rules_path = "/home/user/firewall_rules.txt"

    assert os.path.isfile(script_path), f"Missing {script_path}"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable"

    # Remove rules file if it exists to ensure the script creates it
    if os.path.exists(rules_path):
        os.remove(rules_path)

    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"setup_proxy.sh failed to execute: {result.stderr}"

    assert os.path.isfile(rules_path), f"{rules_path} was not created by setup_proxy.sh"

    with open(rules_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "FORWARD PORT 80 TO ZONE A COST 14",
        "FORWARD PORT 80 TO ZONE B COST 9",
        "FORWARD PORT 80 TO ZONE C COST 18"
    ]

    assert lines == expected_lines, f"Content of {rules_path} does not match expected output. Got: {lines}"

def test_lb_proxy_fuzz_equivalence():
    """Fuzz test lb_proxy.py against oracle_lb_proxy.py."""
    agent_script = "/home/user/lb_proxy.py"
    oracle_script = "/app/oracle_lb_proxy.py"

    assert os.path.isfile(agent_script), f"Missing {agent_script}"
    assert os.path.isfile(oracle_script), f"Missing {oracle_script}"

    random.seed(42)
    N = 500

    for _ in range(N):
        req_id = random.randint(1, 10000)
        size_mb = random.randint(1, 1000)
        input_json = json.dumps({"req_id": req_id, "size_mb": size_mb})

        # Run agent
        agent_cmd = f"bash -c 'source /home/user/.bash_profile && python3 {agent_script} \'{input_json}\''"
        agent_res = subprocess.run(agent_cmd, shell=True, capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {input_json}: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        # Run oracle
        oracle_cmd = f"bash -c 'export ZONE_A_BASE=14; export ZONE_B_BASE=9; export ZONE_C_BASE=18; python3 {oracle_script} \'{input_json}\''"
        oracle_res = subprocess.run(oracle_cmd, shell=True, capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle script failed on input {input_json}: {oracle_res.stderr}"
        oracle_out = oracle_res.stdout.strip()

        assert agent_out == oracle_out, f"Mismatch on input {input_json}. Agent: {agent_out}, Oracle: {oracle_out}"