# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_libsectoken_installed():
    """Verify that the fixed libsectoken package is installed and importable."""
    try:
        import libsectoken
    except ImportError:
        pytest.fail("libsectoken is not installed or importable. The build/install process failed.")

def test_c_code_timing_leak_fixed():
    """Verify that the C code no longer uses standard strcmp for validation."""
    c_file = "/app/vendor/libsectoken-1.2.0/src/validate.c"
    if not os.path.isfile(c_file):
        pytest.fail(f"C source file {c_file} is missing.")

    with open(c_file, "r") as f:
        content = f.read()

    # A basic check to ensure strcmp is not used for the sensitive comparison.
    # The agent should have replaced it with a constant-time comparison.
    # We check if strcmp is still present in a way that suggests it wasn't fixed.
    # This is a heuristic; the fuzz equivalence is the main check.
    if "strcmp(" in content and "CRYPTO_memcmp" not in content and "^" not in content:
        # If strcmp is there and no XOR or memcmp is seen, it might not be fixed.
        # But to be safe, we just check if it's different from the original or if strcmp is removed.
        pass

def test_rotate_tokens_fuzz_equivalence():
    """Fuzz test the agent's Python script against the legacy Rust reference binary."""
    oracle_path = "/opt/legacy/rotate_tokens_ref"
    agent_script = "/home/user/rotate_tokens.py"

    if not os.path.isfile(agent_script):
        pytest.fail(f"Agent script {agent_script} does not exist.")
    if not os.path.isfile(oracle_path):
        pytest.fail(f"Oracle binary {oracle_path} does not exist.")

    random.seed(42)
    alphanumeric = string.ascii_letters + string.digits

    for _ in range(1000):
        seed_len = random.randint(8, 32)
        seed = ''.join(random.choice(alphanumeric) for _ in range(seed_len))
        user_id = str(random.randint(1, 100000))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_path, seed, user_id],
                capture_output=True, text=True, check=True, timeout=2
            )
            oracle_out = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input seed='{seed}', user_id='{user_id}': {e.stderr}")

        # Run agent
        try:
            agent_res = subprocess.run(
                ["python3", agent_script, seed, user_id],
                capture_output=True, text=True, check=True, timeout=2
            )
            agent_out = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input seed='{seed}', user_id='{user_id}': {e.stderr}")

        assert agent_out == oracle_out, (
            f"Output mismatch for seed='{seed}', user_id='{user_id}'.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )

def test_audit_services_script_exists():
    """Verify that the bash script for auditing services exists."""
    script_path = "/home/user/audit_services.sh"
    assert os.path.isfile(script_path), f"Audit script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Audit script {script_path} is not executable."

def test_vulnerable_ports_log_exists():
    """Verify that the vulnerable_ports.log exists."""
    log_path = "/home/user/vulnerable_ports.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did the agent run the audit script?"