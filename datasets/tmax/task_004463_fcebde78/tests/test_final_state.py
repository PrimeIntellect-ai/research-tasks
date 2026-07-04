# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_symlink_created():
    symlink_path = "/home/user/vm-logs"
    target_path = "/tmp/qemu-vms"

    assert os.path.islink(symlink_path) or os.path.islink(symlink_path.rstrip('/')), f"Expected {symlink_path} to be a symbolic link."

    # Resolve the symlink
    actual_target = os.readlink(symlink_path.rstrip('/'))
    # Handle possible trailing slashes
    assert actual_target.rstrip('/') == target_path.rstrip('/'), f"Symlink {symlink_path} points to {actual_target}, expected {target_path}"

def test_pipeline_script_fixes():
    script_path = "/home/user/pipeline/run_cost.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Check that the script no longer relies on relative path for the tool and output
    assert "/home/user/bin/netcost" in content, "Pipeline script does not use the absolute path for the tool (/home/user/bin/netcost)."
    assert "/home/user/reports/cost.out" in content, "Pipeline script does not use the absolute path for the output file (/home/user/reports/cost.out)."

def test_pipeline_script_execution():
    script_path = "/home/user/pipeline/run_cost.sh"
    output_path = "/home/user/reports/cost.out"

    # Remove output file if it exists to ensure we generate a new one
    if os.path.exists(output_path):
        os.remove(output_path)

    # Run script with empty PATH
    env = os.environ.copy()
    env["PATH"] = ""

    result = subprocess.run(["bash", script_path], env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed to execute with empty PATH. Error: {result.stderr}"

    assert os.path.isfile(output_path), f"Output file {output_path} was not created by the pipeline script."

    with open(output_path, "r") as f:
        output_content = f.read().strip()

    assert output_content.isdigit(), f"Output file content '{output_content}' is not a valid integer cost."

def test_fuzz_equivalence():
    agent_tool = "/home/user/bin/netcost"
    oracle_tool = "/opt/oracle/netcost-oracle"

    assert os.path.isfile(agent_tool), f"Agent tool {agent_tool} is missing."
    assert os.access(agent_tool, os.X_OK), f"Agent tool {agent_tool} is not executable."

    assert os.path.isfile(oracle_tool), f"Oracle tool {oracle_tool} is missing."
    assert os.access(oracle_tool, os.X_OK), f"Oracle tool {oracle_tool} is not executable."

    random.seed(42)
    charset = string.ascii_letters + string.digits

    N = 200
    for i in range(N):
        length = random.randint(10, 1000)
        input_str = "".join(random.choices(charset, k=length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_tool],
            input=input_str,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_out = oracle_proc.stdout.strip()

        # Run agent tool
        agent_proc = subprocess.run(
            [agent_tool],
            input=input_str,
            text=True,
            capture_output=True,
            check=True
        )
        agent_out = agent_proc.stdout.strip()

        assert agent_out == oracle_out, (
            f"Mismatch on fuzz iteration {i}.\n"
            f"Input length: {length}\n"
            f"Oracle output: {oracle_out}\n"
            f"Agent output: {agent_out}\n"
            f"Input string: {input_str}"
        )