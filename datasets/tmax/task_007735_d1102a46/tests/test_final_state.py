# test_final_state.py
import os
import re
import socket
import subprocess

def test_operator_fstab():
    fstab_path = "/home/user/operator_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."
    with open(fstab_path, "r") as f:
        content = f.read().strip()
    assert content == "/home/user/source_manifests /home/user/target_state", f"Incorrect content in {fstab_path}."

def test_source_files():
    dep_path = "/home/user/source_manifests/deployment.yaml"
    svc_path = "/home/user/source_manifests/service.yaml"
    assert os.path.isfile(dep_path), f"Source file {dep_path} missing."
    assert os.path.isfile(svc_path), f"Source file {svc_path} missing."
    with open(dep_path, "r") as f:
        assert f.read().strip() == "kind: Deployment", "Incorrect content in source deployment.yaml."
    with open(svc_path, "r") as f:
        assert f.read().strip() == "kind: Service", "Incorrect content in source service.yaml."

def test_target_files():
    dep_path = "/home/user/target_state/deployment.yaml"
    svc_path = "/home/user/target_state/service.yaml"
    assert os.path.isfile(dep_path), f"Target file {dep_path} missing."
    assert os.path.isfile(svc_path), f"Target file {svc_path} missing."

    time_pattern = re.compile(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Applied")

    with open(dep_path, "r") as f:
        dep_content = f.read()
    assert "kind: Deployment" in dep_content, "Missing original content in target deployment.yaml."
    assert time_pattern.search(dep_content), "Missing or incorrect timestamp format in target deployment.yaml."

    with open(svc_path, "r") as f:
        svc_content = f.read()
    assert "kind: Service" in svc_content, "Missing original content in target service.yaml."
    assert time_pattern.search(svc_content), "Missing or incorrect timestamp format in target service.yaml."

def test_c_operator_files():
    assert os.path.isfile("/home/user/operator.c"), "C source file /home/user/operator.c missing."
    assert os.path.isfile("/home/user/operator"), "Compiled executable /home/user/operator missing."
    assert os.access("/home/user/operator", os.X_OK), "/home/user/operator is not executable."

def test_tunnel_log():
    log_path = "/home/user/tunnel_test.log"
    assert os.path.isfile(log_path), f"Log file {log_path} missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert "STATUS: OPERATIONAL" in content, "Tunnel log does not contain 'STATUS: OPERATIONAL'."

def test_ports_listening():
    # Check if anything is listening on 7777 (Operator) and 8888 (SSH Tunnel)
    def is_port_listening(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_listening(7777), "Operator is not listening on port 7777."
    assert is_port_listening(8888), "SSH tunnel is not listening on port 8888."