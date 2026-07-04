# test_final_state.py
import os
import json
import subprocess

def test_script_exists_and_executable():
    script_path = "/home/user/build_restore.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_restore_plan_1():
    plan_path = "/home/user/restore_plan_1.json"
    assert os.path.isfile(plan_path), f"File {plan_path} is missing."

    with open(plan_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {plan_path} does not contain valid JSON."

    assert data.get("target") == "bkp_007", f"Incorrect target in {plan_path}."
    assert data.get("valid") is True, f"Expected valid=true in {plan_path}."
    assert data.get("chain") == ["bkp_001", "bkp_003", "bkp_005", "bkp_006", "bkp_007"], f"Incorrect chain in {plan_path}."
    assert data.get("total_size_mb") == 5555, f"Incorrect total_size_mb in {plan_path}."

def test_restore_plan_2():
    plan_path = "/home/user/restore_plan_2.json"
    assert os.path.isfile(plan_path), f"File {plan_path} is missing."

    with open(plan_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {plan_path} does not contain valid JSON."

    assert data.get("target") == "bkp_009", f"Incorrect target in {plan_path}."
    assert data.get("valid") is False, f"Expected valid=false in {plan_path}."
    assert "chain" not in data, f"chain should not be present in invalid plan {plan_path}."
    assert "total_size_mb" not in data, f"total_size_mb should not be present in invalid plan {plan_path}."

def test_script_dynamic_behavior():
    script_path = "/home/user/build_restore.sh"

    # Test valid target
    result = subprocess.run([script_path, "bkp_002"], capture_output=True, text=True)
    assert result.returncode == 0, "Script failed when running dynamically for bkp_002."

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Script output for bkp_002 is not valid JSON."

    assert data.get("target") == "bkp_002"
    assert data.get("valid") is True
    assert data.get("chain") == ["bkp_001", "bkp_002"]
    assert data.get("total_size_mb") == 5250

    # Test invalid target
    result = subprocess.run([script_path, "bkp_004"], capture_output=True, text=True)
    assert result.returncode == 0, "Script failed when running dynamically for bkp_004."

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        assert False, "Script output for bkp_004 is not valid JSON."

    assert data.get("target") == "bkp_004"
    assert data.get("valid") is False