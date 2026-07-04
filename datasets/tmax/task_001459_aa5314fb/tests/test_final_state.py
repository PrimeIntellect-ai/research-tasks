# test_final_state.py
import os
import pwd

def test_edge_config_exists():
    assert os.path.isfile("/home/user/edge_config.txt"), "/home/user/edge_config.txt does not exist."
    with open("/home/user/edge_config.txt", "r") as f:
        content = f.read()
    assert "MAC=52:54:00:11:22:33" in content, "MAC address not found in edge_config.txt"
    assert "VNC_DISPLAY=4" in content, "VNC_DISPLAY not found in edge_config.txt"
    assert "GUEST_PORT=80" in content, "GUEST_PORT not found in edge_config.txt"
    assert "HOST_PORT=8080" in content, "HOST_PORT not found in edge_config.txt"

def test_rust_source_exists():
    assert os.path.isfile("/home/user/build_edge_node.rs"), "/home/user/build_edge_node.rs does not exist."

def test_rust_binary_exists_and_executable():
    binary_path = "/home/user/build_edge_node"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_run_vm_script_exists_and_executable():
    script_path = "/home/user/run_vm.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_run_vm_script_content():
    try:
        user_uid = pwd.getpwnam("user").pw_uid
    except KeyError:
        assert False, "User 'user' does not exist in the system."

    expected_cmd = (
        f"qemu-system-x86_64 -m 256 -vnc 127.0.0.1:4 "
        f"-netdev user,id=net0,hostfwd=tcp::8080-:80 "
        f"-device virtio-net-pci,netdev=net0,mac=52:54:00:11:22:33 "
        f"-fw_cfg name=opt/edge_uid,string={user_uid}"
    )

    with open("/home/user/run_vm.sh", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith("#")]

    assert len(lines) == 1, "run_vm.sh should contain exactly one line of command (excluding comments and empty lines)."
    actual_cmd = lines[0]

    assert actual_cmd == expected_cmd, f"run_vm.sh content mismatch.\nExpected: {expected_cmd}\nGot: {actual_cmd}"