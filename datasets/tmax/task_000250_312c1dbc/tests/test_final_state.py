# test_final_state.py

import os
import json
import random
import subprocess
import pytest

def test_agent_executable_exists():
    agent_exe = "/home/user/time_series_filter"
    assert os.path.isfile(agent_exe), f"The compiled executable {agent_exe} is missing."
    assert os.access(agent_exe, os.X_OK), f"The file {agent_exe} is not executable."

def test_fuzz_equivalence():
    agent_exe = "/home/user/time_series_filter"
    oracle_exe = "/app/oracle_time_series_filter"

    assert os.path.isfile(oracle_exe), f"Oracle executable {oracle_exe} is missing."

    random.seed(42)

    # Ensure the vendored shared library can be found if dynamically linked
    env = os.environ.copy()
    cjson_lib_path = "/app/cJSON-1.7.15"
    if "LD_LIBRARY_PATH" in env:
        env["LD_LIBRARY_PATH"] = f"{cjson_lib_path}:{env['LD_LIBRARY_PATH']}"
    else:
        env["LD_LIBRARY_PATH"] = cjson_lib_path

    for i in range(500):
        num_elements = random.randint(1, 100)

        # Generate strictly monotonically increasing timestamps
        arr = []
        current_time = random.uniform(1500000000.000000, 1690000000.000000)
        for _ in range(num_elements):
            arr.append(round(current_time, 6))
            current_time += random.uniform(0.000001, 1000.0)

        input_json = json.dumps(arr)

        oracle_proc = subprocess.run(
            [oracle_exe, input_json],
            capture_output=True,
            text=True,
            env=env
        )

        agent_proc = subprocess.run(
            [agent_exe, input_json],
            capture_output=True,
            text=True,
            env=env
        )

        assert oracle_proc.returncode == agent_proc.returncode, (
            f"Return code mismatch on iteration {i}.\n"
            f"Input: {input_json}\n"
            f"Oracle return code: {oracle_proc.returncode}\n"
            f"Agent return code: {agent_proc.returncode}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        assert oracle_proc.stdout == agent_proc.stdout, (
            f"Output mismatch on iteration {i}.\n"
            f"Input: {input_json}\n"
            f"Oracle stdout:\n{oracle_proc.stdout}\n"
            f"Agent stdout:\n{agent_proc.stdout}\n"
        )