# test_final_state.py

import os
import stat
import subprocess
import random
import string
import pytest

def test_deployment_state():
    """Verify the deployment script and the resulting file system state."""
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"Deploy script missing: {deploy_script}"
    assert os.access(deploy_script, os.X_OK) or os.access(deploy_script, os.R_OK), "Deploy script must be readable or executable"

    # Run the deploy script again to check idempotency
    result = subprocess.run(["bash", deploy_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Deploy script failed on subsequent run:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Check directories and permissions
    dirs_to_check = [
        "/home/user/deploy",
        "/home/user/deploy/staging",
        "/home/user/deploy/staging/bin",
        "/home/user/deploy/production",
        "/home/user/deploy/production/bin",
    ]
    for d in dirs_to_check:
        assert os.path.isdir(d), f"Directory missing: {d}"
        mode = stat.S_IMODE(os.stat(d).st_mode)
        assert mode == 0o755, f"Directory {d} has incorrect permissions: {oct(mode)} (expected 0o755)"

    # Check deployed binaries and permissions
    binaries_to_check = [
        "/home/user/deploy/staging/bin/dashboard_parser",
        "/home/user/deploy/production/bin/dashboard_parser",
    ]
    for b in binaries_to_check:
        assert os.path.isfile(b), f"Deployed binary missing: {b}"
        mode = stat.S_IMODE(os.stat(b).st_mode)
        assert mode == 0o555, f"Binary {b} has incorrect permissions: {oct(mode)} (expected 0o555)"

def generate_random_input():
    """Generates a random input string matching the specified format."""
    num_pairs = random.randint(10, 100)
    pairs = []
    for _ in range(num_pairs):
        str_len = random.randint(3, 8)
        subsystem = "".join(random.choices(string.ascii_uppercase, k=str_len))
        # Include specific subsystems to ensure logic is tested
        if random.random() < 0.2:
            subsystem = random.choice(["CPU", "DISK", "NETWORK"])

        value = random.randint(-2147483648, 2147483647)
        pairs.append(f"{subsystem} {value}")

    return " ".join(pairs)

def test_fuzz_equivalence():
    """Fuzz test the deployed binary against the oracle."""
    oracle_path = "/app/oracle_parser"
    agent_path = "/home/user/deploy/production/bin/dashboard_parser"

    assert os.path.isfile(oracle_path), f"Oracle missing: {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary missing: {agent_path}"

    random.seed(42)
    num_tests = 10000

    for i in range(num_tests):
        test_input = generate_random_input()

        oracle_proc = subprocess.run(
            [oracle_path],
            input=test_input,
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input: {test_input}"

        agent_proc = subprocess.run(
            [agent_path],
            input=test_input,
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == 0, f"Agent failed on input: {test_input}\nSTDERR: {agent_proc.stderr}"

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Output mismatch on test {i+1}/{num_tests}.\n"
            f"Input:\n{test_input}\n\n"
            f"Expected (Oracle):\n{oracle_proc.stdout}\n\n"
            f"Actual (Agent):\n{agent_proc.stdout}"
        )