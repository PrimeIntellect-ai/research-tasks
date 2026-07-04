# test_final_state.py

import os
import json
import subprocess
import pytest

def test_jsd_original():
    path = "/home/user/jsd_original.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: {content}")

    assert val > 0.0, f"JSD for original runs should be > 0, but got {val}"

def test_jsd_fixed():
    path = "/home/user/jsd_fixed.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid float: {content}")

    assert val == 0.0, f"JSD for fixed runs should be exactly 0.0, but got {val}"

def test_simulate_diffusion_deterministic():
    script_path = "/home/user/simulate_diffusion.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    env1 = os.environ.copy()
    env1["PYTHONHASHSEED"] = "1"

    env2 = os.environ.copy()
    env2["PYTHONHASHSEED"] = "2"

    try:
        res1 = subprocess.run(
            ["python3", script_path],
            env=env1,
            capture_output=True,
            text=True,
            check=True,
            cwd="/home/user"
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with PYTHONHASHSEED=1:\n{e.stderr}")

    try:
        res2 = subprocess.run(
            ["python3", script_path],
            env=env2,
            capture_output=True,
            text=True,
            check=True,
            cwd="/home/user"
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed with PYTHONHASHSEED=2:\n{e.stderr}")

    try:
        out1 = json.loads(res1.stdout)
    except json.JSONDecodeError:
        pytest.fail("Output from first run is not valid JSON.")

    try:
        out2 = json.loads(res2.stdout)
    except json.JSONDecodeError:
        pytest.fail("Output from second run is not valid JSON.")

    assert out1 == out2, "The output of simulate_diffusion.py is not deterministic across different PYTHONHASHSEED values."