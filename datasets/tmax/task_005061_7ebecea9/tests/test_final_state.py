# test_final_state.py

import os
import json
import random
import string
import subprocess
import pytest

REPORT_PATH = "/home/user/investigation_report.json"
ORACLE_PATH = "/app/oracle_sanitizer"
AGENT_SCRIPT = "/home/user/sanitizer.py"

def test_investigation_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Missing investigation report at {REPORT_PATH}"

def test_investigation_report_contents():
    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report at {REPORT_PATH} is not valid JSON")

    expected_keys = ["dropped_elf_filename", "backdoor_port", "altered_file", "rogue_issuer_cn"]
    for key in expected_keys:
        assert key in report, f"Missing key '{key}' in investigation report"

    assert report["dropped_elf_filename"] == "sys_updater.elf", \
        f"Expected dropped_elf_filename to be 'sys_updater.elf', got '{report['dropped_elf_filename']}'"

    assert report["backdoor_port"] == 6667, \
        f"Expected backdoor_port to be 6667, got {report['backdoor_port']}"

    assert report["altered_file"] == "config/settings.yml", \
        f"Expected altered_file to be 'config/settings.yml', got '{report['altered_file']}'"

    assert report["rogue_issuer_cn"] == "EvilCorp Root CA", \
        f"Expected rogue_issuer_cn to be 'EvilCorp Root CA', got '{report['rogue_issuer_cn']}'"

def test_sanitizer_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Missing agent script at {AGENT_SCRIPT}"

def generate_fuzz_inputs(n=1000):
    # Fuzz-input distribution: Random strings of length 1 to 200 containing alphanumeric characters 
    # and frequent directory traversal sequences.
    random.seed(42)
    alphanumeric = string.ascii_letters + string.digits
    traversal_seqs = ["../", "..\\", "./", "//", "%2e%2e%2f"]

    inputs = []
    for _ in range(n):
        length = random.randint(1, 200)
        res = []
        while len(res) < length:
            if random.random() < 0.3:
                res.append(random.choice(traversal_seqs))
            else:
                res.append(random.choice(alphanumeric))

        # Join and truncate to exact length
        fuzz_str = "".join(res)[:length]
        inputs.append(fuzz_str)

    return inputs

def test_fuzz_equivalence_sanitizer():
    # We test 1000 inputs to keep test execution time reasonable while still providing strong equivalence guarantees.
    inputs = generate_fuzz_inputs(n=1000)

    for fuzz_input in inputs:
        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=fuzz_input,
            text=True,
            capture_output=True
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT],
            input=fuzz_input,
            text=True,
            capture_output=True
        )
        agent_out = agent_proc.stdout

        assert oracle_out == agent_out, (
            f"Output mismatch on input: {repr(fuzz_input)}\n"
            f"Oracle output: {repr(oracle_out)}\n"
            f"Agent output:  {repr(agent_out)}"
        )