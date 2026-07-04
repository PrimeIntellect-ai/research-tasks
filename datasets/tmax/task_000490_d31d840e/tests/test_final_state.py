# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/net_health_checker"
AGENT_SCRIPT = "/home/user/net_health_checker.py"
LOGROTATE_CONF = "/home/user/logrotate.d/net_health"

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def generate_random_timestamp():
    year = random.randint(2020, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

def generate_random_log_file(path, num_lines):
    statuses = ["SUCCESS", "TIMEOUT", "REFUSED", "ERROR", "PENDING"]
    with open(path, "w") as f:
        for _ in range(num_lines):
            if random.random() < 0.1:
                # Malformed line
                f.write("".join(random.choices(string.ascii_letters + string.digits + " []-:", k=random.randint(10, 50))) + "\n")
            else:
                timestamp = generate_random_timestamp()
                ip = generate_random_ip()
                port = random.randint(1, 65535)
                status = random.choice(statuses)
                f.write(f"[{timestamp}] {ip} {port} {status}\n")

def test_logrotate_config():
    assert os.path.exists(LOGROTATE_CONF), f"Logrotate config missing at {LOGROTATE_CONF}"
    with open(LOGROTATE_CONF, "r") as f:
        content = f.read()

    assert "daily" in content, "Logrotate config missing 'daily'"
    assert "rotate 7" in content, "Logrotate config missing 'rotate 7'"
    assert "compress" in content, "Logrotate config missing 'compress'"
    assert "create 0644" in content, "Logrotate config missing 'create 0644'"

def test_agent_script_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable"

def run_program(executable, arg):
    cmd = [executable, arg]
    if executable.endswith(".py"):
        cmd = ["python3", executable, arg]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"

def test_fuzz_equivalence():
    random.seed(42)

    # Test non-existent file
    oracle_code, oracle_out, oracle_err = run_program(ORACLE_PATH, "/non_existent_file.log")
    agent_code, agent_out, agent_err = run_program(AGENT_SCRIPT, "/non_existent_file.log")

    assert agent_code == oracle_code, f"Exit code mismatch on non-existent file. Oracle: {oracle_code}, Agent: {agent_code}"
    assert agent_out == oracle_out, "Stdout mismatch on non-existent file."
    assert agent_err == oracle_err, "Stderr mismatch on non-existent file."

    # Fuzz tests
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(100):
            num_lines = random.randint(0, 1000)
            log_path = os.path.join(tmpdir, f"test_{i}.log")
            generate_random_log_file(log_path, num_lines)

            oracle_code, oracle_out, oracle_err = run_program(ORACLE_PATH, log_path)
            agent_code, agent_out, agent_err = run_program(AGENT_SCRIPT, log_path)

            assert agent_code == oracle_code, f"Exit code mismatch on test {i} (lines: {num_lines}). Oracle: {oracle_code}, Agent: {agent_code}"
            assert agent_out == oracle_out, f"Stdout mismatch on test {i} (lines: {num_lines}).\nOracle:\n{oracle_out}\nAgent:\n{agent_out}"
            assert agent_err == oracle_err, f"Stderr mismatch on test {i} (lines: {num_lines}).\nOracle:\n{oracle_err}\nAgent:\n{agent_err}"