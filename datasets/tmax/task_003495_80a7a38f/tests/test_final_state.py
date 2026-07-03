# test_final_state.py

import os
import subprocess
import random
import pytest

def test_setup_complete_log():
    log_path = "/home/user/setup_complete.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "DONE", f"Expected 'DONE' in {log_path}, but got '{content}'."

def test_bridge_script_executable():
    script_path = "/home/user/bridge.sh"
    assert os.path.isfile(script_path), f"Bridge script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Bridge script {script_path} is not executable."

def test_metric_parser_executable():
    parser_path = "/home/user/metric_parser"
    assert os.path.isfile(parser_path), f"Metric parser {parser_path} is missing."
    assert os.access(parser_path, os.X_OK), f"Metric parser {parser_path} is not executable."

def test_metric_parser_fuzz_equivalence():
    agent_parser = "/home/user/metric_parser"
    oracle_parser = "/app/bin/oracle_parser"

    assert os.path.isfile(agent_parser), f"Agent parser {agent_parser} is missing."
    assert os.path.isfile(oracle_parser), f"Oracle parser {oracle_parser} is missing."

    random.seed(42)

    for _ in range(1000):
        uptime = random.randint(0, 99999)
        cpu = random.randint(0, 999)
        mem = random.randint(0, 999)
        test_input = f"UPTIME:{uptime}:CPU:{cpu}:MEM:{mem}\n"

        agent_proc = subprocess.run(
            [agent_parser],
            input=test_input,
            text=True,
            capture_output=True
        )
        oracle_proc = subprocess.run(
            [oracle_parser],
            input=test_input,
            text=True,
            capture_output=True
        )

        agent_out = agent_proc.stdout
        oracle_out = oracle_proc.stdout

        assert agent_out == oracle_out, (
            f"Output mismatch for input: {test_input!r}\n"
            f"Expected (Oracle): {oracle_out!r}\n"
            f"Got (Agent): {agent_out!r}\n"
            f"Agent stderr: {agent_proc.stderr!r}"
        )