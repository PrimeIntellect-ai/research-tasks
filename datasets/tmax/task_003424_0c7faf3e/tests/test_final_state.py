# test_final_state.py

import os
import random
import subprocess
import pytest

def test_construct_init_perturbation_removed():
    """Verify that the anti-analysis perturbation has been removed from the vendored construct package."""
    init_file = "/app/construct-2.10.68/construct/__init__.py"
    assert os.path.exists(init_file), f"The file {init_file} is missing."

    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()

    expected_string = 'raise RuntimeError("Anti-analysis protection triggered")'
    assert expected_string not in content, f"The expected anti-analysis perturbation is still present in {init_file}."

def test_process_alert_script_exists():
    """Verify that the student has created the required Python script."""
    script_path = "/home/user/process_alert.py"
    assert os.path.exists(script_path), f"The script {script_path} is missing."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def generate_fuzz_inputs(n=1000):
    """Generate N random hex strings, with ~20% seeded to heavily exercise the parsing/cracking logic."""
    random.seed(42)
    inputs = []
    for i in range(n):
        if i < n * 0.2:
            # 20% seeded: must contain "494453" (3 bytes) + 4 bytes = 7 bytes minimum.
            total_bytes = random.randint(7, 50)
            prefix_bytes = random.randint(0, total_bytes - 7)
            suffix_bytes = total_bytes - 7 - prefix_bytes

            prefix = "".join(random.choice("0123456789ABCDEF") for _ in range(prefix_bytes * 2))
            marker = "494453"
            payload = "".join(random.choice("0123456789ABCDEF") for _ in range(8))
            suffix = "".join(random.choice("0123456789ABCDEF") for _ in range(suffix_bytes * 2))

            inputs.append(prefix + marker + payload + suffix)
        else:
            # Random hex strings of length 5 to 50 bytes
            length = random.randint(5, 50) * 2
            inputs.append("".join(random.choice("0123456789ABCDEF") for _ in range(length)))

    # Shuffle to mix seeded and unseeded inputs
    random.shuffle(inputs)
    return inputs

def test_fuzz_equivalence():
    """Test that the agent's Python script behaves bit-exactly identically to the oracle binary on N random inputs."""
    oracle_path = "/app/bin/alert_processor"
    agent_script = "/home/user/process_alert.py"

    assert os.path.exists(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    inputs = generate_fuzz_inputs(1000)

    env = os.environ.copy()
    # Ensure the vendored construct package is in PYTHONPATH
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"/app/construct-2.10.68:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = "/app/construct-2.10.68"

    for hex_input in inputs:
        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path, hex_input],
            capture_output=True,
            text=True
        )

        # Run agent script
        agent_proc = subprocess.run(
            ["python3", agent_script, hex_input],
            capture_output=True,
            text=True,
            env=env
        )

        # Assert exact equivalence
        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Stdout mismatch on input: {hex_input}\n"
            f"Oracle output: {repr(oracle_proc.stdout)}\n"
            f"Agent output:  {repr(agent_proc.stdout)}"
        )

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on input: {hex_input}\n"
            f"Oracle return code: {oracle_proc.returncode}\n"
            f"Agent return code:  {agent_proc.returncode}\n"
            f"Oracle stderr: {repr(oracle_proc.stderr)}\n"
            f"Agent stderr:  {repr(agent_proc.stderr)}"
        )