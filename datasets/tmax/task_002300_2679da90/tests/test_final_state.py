# test_final_state.py
import os
import stat
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    """Fuzz the agent's python script against the oracle."""
    agent_script = "/home/user/health_eval.py"
    oracle_script = "/app/oracle_health_eval"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"

    random.seed(42)

    for _ in range(1000):
        # Generate IPv4
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
        # Generate latency
        latency = str(random.randint(0, 20000))

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script, ip, latency],
            capture_output=True,
            text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on inputs: {ip} {latency}\nStderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_script, ip, latency],
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle script failed on inputs: {ip} {latency}\nStderr: {oracle_proc.stderr}"
        oracle_out = oracle_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on inputs IPv4={ip}, Latency={latency}.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )

def test_deployment_script_artifacts():
    """Check the deployed file and permissions."""
    deployed_script = "/home/user/health_checks/bin/health_eval.py"
    assert os.path.isfile(deployed_script), f"Deployed script missing: {deployed_script}"

    st = os.stat(deployed_script)
    # Check if permissions are at least 755 (or exactly 755)
    # 755 in octal is 0o755
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o755, f"Deployed script permissions are {oct(perms)}, expected 0o755"

def test_cron_job_idempotent():
    """Check the crontab for exactly one matching entry."""
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab: {e.stderr}")

    expected_command_parts = [
        "*/5 * * * *",
        "/home/user/health_checks/bin/health_eval.py",
        "10.0.0.1",
        "500"
    ]

    match_count = 0
    for line in crontab_output.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Check if all expected parts are in the line
        if all(part in line for part in expected_command_parts):
            match_count += 1

    assert match_count > 0, "Cron job entry not found."
    assert match_count == 1, f"Cron job entry is duplicated. Found {match_count} matches, expected exactly 1."