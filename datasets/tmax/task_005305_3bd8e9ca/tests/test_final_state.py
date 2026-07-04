# test_final_state.py
import os
import subprocess
import random
import pytest

def test_supervisord_services_running():
    conf_path = "/home/user/supervisord.conf"
    assert os.path.isfile(conf_path), f"supervisord.conf missing: {conf_path}"

    # Check if supervisorctl can connect and get status
    result = subprocess.run(
        ["supervisorctl", "-c", conf_path, "status"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"supervisorctl status failed. Is supervisord running? Error: {result.stderr}"

    status_output = result.stdout

    # Verify both services are in RUNNING state
    for service in ["cert-generator", "dashboard-web"]:
        assert service in status_output, f"Service {service} not found in supervisorctl status."
        # Find the line for the service
        line = next(l for l in status_output.splitlines() if service in l)
        assert "RUNNING" in line, f"Service {service} is not RUNNING. Status line: {line}"

    # Verify the certificates were actually generated
    assert os.path.isfile("/home/user/cert.pem"), "/home/user/cert.pem was not generated."
    assert os.path.isfile("/home/user/key.pem"), "/home/user/key.pem was not generated."

def test_analyze_link_fuzz():
    agent_script = "/home/user/analyze_link.py"
    oracle_script = "/app/oracle_analyze_link.py"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"

    random.seed(42)
    num_fuzz_inputs_N = 50

    for _ in range(num_fuzz_inputs_N):
        arg1 = random.randint(0, 299)
        arg2 = random.randint(0, 255)

        oracle_cmd = ["python3", oracle_script, str(arg1), str(arg2)]
        agent_cmd = ["python3", agent_script, str(arg1), str(arg2)]

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on args {arg1} {arg2}: {oracle_res.stderr}"
        assert agent_res.returncode == 0, f"Agent script failed on args {arg1} {arg2}: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Mismatch on frame {arg1}, threshold {arg2}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )