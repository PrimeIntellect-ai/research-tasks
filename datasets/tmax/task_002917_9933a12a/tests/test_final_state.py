# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_ext4_image():
    img_path = "/home/user/data.img"
    assert os.path.exists(img_path), f"Missing image at {img_path}"

    # Check size is approx 10MB
    size = os.path.getsize(img_path)
    assert 9 * 1024 * 1024 <= size <= 11 * 1024 * 1024, f"Image size {size} is not ~10MB"

    # Check ext4 magic number at offset 0x438
    with open(img_path, "rb") as f:
        f.seek(0x438)
        magic = f.read(2)
        assert magic == b"\x53\xef", "File does not appear to be a valid ext2/3/4 filesystem (magic number mismatch)"

def test_data_mount_dir():
    mount_dir = "/home/user/data_mount"
    assert os.path.isdir(mount_dir), f"Missing mount directory at {mount_dir}"

def test_fstab_entry():
    fstab_path = "/home/user/fstab_entry"
    assert os.path.exists(fstab_path), f"Missing fstab entry file at {fstab_path}"
    with open(fstab_path, "r") as f:
        content = f.read().strip()

    parts = content.split()
    assert len(parts) >= 4, "fstab entry does not have enough fields"
    assert "/home/user/data.img" in parts[0] or "/home/user/data.img" in content, "fstab entry missing image path"
    assert "/home/user/data_mount" in parts[1] or "/home/user/data_mount" in content, "fstab entry missing mount point"
    assert "ext4" in parts[2] or "ext4" in content, "fstab entry missing ext4 filesystem type"

def test_sensor_env():
    env_path = "/home/user/sensor_env.sh"
    assert os.path.exists(env_path), f"Missing env script at {env_path}"
    with open(env_path, "r") as f:
        content = f.read()
    assert "Europe/Berlin" in content, "TZ environment variable is not set to Europe/Berlin"
    assert "en_US.UTF-8" in content, "LANG environment variable is not set to en_US.UTF-8"

def test_ssh_tunnel_cmd():
    cmd_path = "/home/user/ssh_tunnel_cmd.txt"
    assert os.path.exists(cmd_path), f"Missing SSH tunnel command file at {cmd_path}"
    with open(cmd_path, "r") as f:
        content = f.read()
    assert "-L" in content, "SSH command missing -L flag for port forwarding"
    assert "8080" in content, "SSH command missing local port 8080"
    assert "9090" in content, "SSH command missing target port 9090"

def test_expect_script():
    script_path = "/home/user/automate_setup.exp"
    assert os.path.exists(script_path), f"Missing expect script at {script_path}"

    # Run the expect script and see if it successfully interacts with the legacy binary
    res = subprocess.run(["expect", script_path], capture_output=True, text=True)
    assert res.returncode == 0, f"Expect script failed with return code {res.returncode}. Output: {res.stdout}\n{res.stderr}"
    assert "Setup complete" in res.stdout, f"Expect script did not complete setup successfully. Output: {res.stdout}"

def test_fuzz_equivalence():
    oracle = "/app/legacy_sensor_bin"
    agent = "/home/user/process_sensor"

    assert os.path.exists(agent), f"Agent program {agent} not found"
    assert os.access(agent, os.X_OK), f"Agent program {agent} is not executable"

    random.seed(42)
    # Printable ASCII excluding newlines
    chars = string.ascii_letters + string.digits + string.punctuation + " "

    for i in range(100):
        length = random.randint(1, 100)
        inp = "".join(random.choices(chars, k=length))

        oracle_proc = subprocess.run([oracle], input=inp, text=True, capture_output=True)
        agent_proc = subprocess.run([agent], input=inp, text=True, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input {inp!r}"

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        assert oracle_out == agent_out, (
            f"Output mismatch on fuzz iteration {i}.\n"
            f"Input: {inp!r}\n"
            f"Oracle output: {oracle_out!r}\n"
            f"Agent output: {agent_out!r}"
        )