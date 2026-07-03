# test_final_state.py
import os
import random
import string
import subprocess

def test_log_file_created():
    log_path = "/var/log/health.log"
    assert os.path.isfile(log_path), f"Missing dummy log file at {log_path}"

def test_logrotate_config():
    config_path = "/etc/logrotate.d/health_monitor"
    assert os.path.isfile(config_path), f"Missing logrotate config at {config_path}"

    with open(config_path, "r") as f:
        content = f.read()

    # Check for required directives
    assert "/var/log/health.log" in content, "Logrotate config does not specify /var/log/health.log"
    assert "daily" in content, "Logrotate config missing 'daily' directive"
    assert "rotate 7" in content, "Logrotate config missing 'rotate 7' directive"
    assert "compress" in content, "Logrotate config missing 'compress' directive"

def test_agent_script_exists_and_executable():
    script_path = "/home/user/log_filter"
    assert os.path.isfile(script_path), f"Missing script at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_filter"
    agent_path = "/home/user/log_filter"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle at {oracle_path} is not executable"

    random.seed(42)
    inputs = []
    for _ in range(500):
        base_len = random.randint(0, 200)
        base_str = ''.join(random.choices(string.ascii_letters + string.digits, k=base_len))
        num_errors = random.randint(0, 10)

        for _ in range(num_errors):
            insert_pos = random.randint(0, len(base_str))
            base_str = base_str[:insert_pos] + "ERROR" + base_str[insert_pos:]
        inputs.append(base_str)

    for i, test_input in enumerate(inputs):
        # Run oracle
        proc_oracle = subprocess.run(
            [oracle_path],
            input=test_input,
            text=True,
            capture_output=True
        )
        oracle_out = proc_oracle.stdout

        # Run agent
        proc_agent = subprocess.run(
            [agent_path],
            input=test_input,
            text=True,
            capture_output=True
        )
        agent_out = proc_agent.stdout

        assert oracle_out == agent_out, (
            f"Mismatch on fuzz iteration {i}.\n"
            f"Input: {repr(test_input)}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output: {repr(agent_out)}"
        )