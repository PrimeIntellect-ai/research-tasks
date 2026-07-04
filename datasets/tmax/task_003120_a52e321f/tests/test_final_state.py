# test_final_state.py

import os
import json
import subprocess
import tempfile
import shutil
import pytest

def test_phase1_active_capacity():
    cap_file = "/home/user/active_capacity.txt"
    assert os.path.isfile(cap_file), f"File {cap_file} is missing. Phase 1 incomplete."

    with open(cap_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"Expected 2 lines in {cap_file}, found {len(lines)}"

    expected_cpu = "ACTIVE_CPU: 30"
    expected_ram = "ACTIVE_RAM: 61440"

    assert expected_cpu in lines, f"Missing or incorrect CPU total. Expected '{expected_cpu}'"
    assert expected_ram in lines, f"Missing or incorrect RAM total. Expected '{expected_ram}'"

def test_phase2_git_hook_executable():
    hook_path = "/home/user/infra.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"Git hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook at {hook_path} is not executable"

def test_phase2_git_hook_enforcement():
    workspace = "/home/user/infra_workspace"
    assert os.path.isdir(workspace), f"Workspace {workspace} missing"

    # Test rejection (CPU > 200)
    # Active CPU is 30, so adding 171 makes it 201 > 200
    reject_vms = [{"name": "huge", "cpu": 171, "ram": 1024, "env": "dev"}]
    vms_file = os.path.join(workspace, "vms.json")

    with open(vms_file, "w") as f:
        json.dump(reject_vms, f)

    subprocess.run(["git", "add", "vms.json"], cwd=workspace, check=True)
    subprocess.run(["git", "commit", "-m", "test reject"], cwd=workspace, check=True)

    push_result = subprocess.run(
        ["git", "push", "origin", "master"],
        cwd=workspace,
        capture_output=True,
        text=True
    )

    assert push_result.returncode != 0, "Git push should have been rejected by the pre-receive hook"
    assert "CAPACITY EXCEEDED" in push_result.stderr, "Hook did not print 'CAPACITY EXCEEDED' to stderr"

    # Reset commit
    subprocess.run(["git", "reset", "--hard", "HEAD~1"], cwd=workspace, check=True)

    # Test acceptance (CPU <= 200)
    # Active CPU is 30, adding 100 makes it 130 <= 200
    accept_vms = [{"name": "ok", "cpu": 100, "ram": 1024, "env": "dev"}]
    with open(vms_file, "w") as f:
        json.dump(accept_vms, f)

    subprocess.run(["git", "add", "vms.json"], cwd=workspace, check=True)
    subprocess.run(["git", "commit", "-m", "test accept"], cwd=workspace, check=True)

    push_result2 = subprocess.run(
        ["git", "push", "origin", "master"],
        cwd=workspace,
        capture_output=True,
        text=True
    )

    assert push_result2.returncode == 0, f"Git push should have been accepted, but failed: {push_result2.stderr}"

def test_phase3_roll_deploy():
    script_path = "/home/user/roll_deploy.py"
    assert os.path.isfile(script_path), f"Deployment script missing at {script_path}"

    test_vms = [
        {"name": "test1", "cpu": 2, "ram": 1024, "env": "dev"},
        {"name": "test2", "cpu": 4, "ram": 2048, "env": "prod"}
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        json.dump(test_vms, tmp)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            ["python3", script_path, tmp_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"roll_deploy.py failed with error: {result.stderr}"

        stage1_conf = "/home/user/deployments/stage_1/test1.conf"
        stage2_conf = "/home/user/deployments/stage_2/test2.conf"

        assert os.path.isfile(stage1_conf), f"Missing {stage1_conf}"
        assert os.path.isfile(stage2_conf), f"Missing {stage2_conf}"

        with open(stage1_conf, "r") as f:
            assert f.read().strip() == "cpu=2,ram=1024", f"Incorrect content in {stage1_conf}"

        with open(stage2_conf, "r") as f:
            assert f.read().strip() == "cpu=4,ram=2048", f"Incorrect content in {stage2_conf}"

    finally:
        os.remove(tmp_path)