# test_final_state.py
import os
import subprocess

def test_deploy_auth_log():
    log_path = "/home/user/deploy_auth.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_users = ["xena", "yusuf", "zane"]
    assert lines == expected_users, f"Expected users {expected_users} in {log_path}, but got {lines}."

def test_deployment_log():
    log_path = "/home/user/deployment.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "Node 1 deployed successfully",
        "Node 2 deployed successfully",
        "Node 3 deployed successfully"
    ]
    assert lines == expected_lines, f"Expected lines {expected_lines} in {log_path}, but got {lines}."

def test_node_deployments():
    payload_path = "/home/user/update_payload.py"
    assert os.path.isfile(payload_path), f"Original payload {payload_path} is missing."

    with open(payload_path, "r") as f:
        expected_payload = f.read()

    for i in range(1, 4):
        node_dir = f"/home/user/nodes/node{i}"
        assert os.path.isdir(node_dir), f"Directory {node_dir} is missing."

        # Check app.py
        app_path = os.path.join(node_dir, "app.py")
        assert os.path.isfile(app_path), f"File {app_path} is missing."
        with open(app_path, "r") as f:
            app_content = f.read()
        assert app_content == expected_payload, f"Content of {app_path} does not match {payload_path}."

        # Check disk_backup.qcow2
        backup_path = os.path.join(node_dir, "disk_backup.qcow2")
        assert os.path.isfile(backup_path), f"File {backup_path} is missing."

        # Verify qcow2 backing file
        result = subprocess.run(["qemu-img", "info", backup_path], capture_output=True, text=True)
        assert result.returncode == 0, f"qemu-img info failed on {backup_path}. Is qemu-utils installed?"

        output = result.stdout
        assert "file format: qcow2" in output, f"{backup_path} is not a valid qcow2 file."
        assert "backing file: disk.qcow2" in output or "backing file: /home/user/nodes/node" in output, \
            f"{backup_path} is not backed by disk.qcow2. qemu-img info output:\n{output}"